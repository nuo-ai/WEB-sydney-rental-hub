import os
import sys
import logging
import subprocess
from datetime import datetime, timezone
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.executors.pool import ThreadPoolExecutor
import signal

# 处理 dotenv 导入
try:
    from dotenv import load_dotenv
    DOTENV_AVAILABLE = True
except ImportError:
    logging.warning("python-dotenv not available.")
    DOTENV_AVAILABLE = False
    def load_dotenv(*args, **kwargs):
        pass

# Configure detailed logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scheduler.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path, override=True)
    logger.info(f"Successfully loaded .env file from: {dotenv_path}")
else:
    load_dotenv(override=True)
    logger.warning(f".env file not found at {dotenv_path}. Using system environment.")

class PropertyDataScheduler:
    """房源数据自动化调度器"""
    
    def __init__(self):
        self.scheduler = None
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.project_root = os.path.join(self.script_dir, '..')
        
        # 配置调度器
        executors = {
            'default': ThreadPoolExecutor(max_workers=2)
        }
        
        job_defaults = {
            'coalesce': True,  # 如果有多个相同任务排队，只保留最新的一个
            'max_instances': 1,  # 每个任务最多只能有一个实例在运行
            'misfire_grace_time': 300  # 错过执行时间5分钟内仍可执行
        }
        
        self.scheduler = BlockingScheduler(
            executors=executors,
            job_defaults=job_defaults,
            timezone='Australia/Sydney'
        )
        
        # 设置信号处理器用于优雅关闭
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
    def _signal_handler(self, signum, frame):
        """处理关闭信号"""
        logger.info(f"Received signal {signum}, shutting down scheduler...")
        if self.scheduler and self.scheduler.running:
            self.scheduler.shutdown(wait=True)
        sys.exit(0)
        
    def run_spider(self):
        """执行爬虫脚本"""
        logger.info("Starting spider execution...")
        
        try:
            # 切换到项目根目录执行爬虫
            spider_script = os.path.join(self.project_root, 'v2.py')
            
            if not os.path.exists(spider_script):
                logger.error(f"Spider script not found: {spider_script}")
                return False
                
            # 执行爬虫脚本
            result = subprocess.run(
                [sys.executable, spider_script],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=1800  # 30分钟超时
            )
            
            if result.returncode == 0:
                logger.info("Spider execution completed successfully")
                logger.info(f"Spider output: {result.stdout}")
                return True
            else:
                logger.error(f"Spider execution failed with return code {result.returncode}")
                logger.error(f"Spider error: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            logger.error("Spider execution timed out (30 minutes)")
            return False
        except Exception as e:
            logger.error(f"Error running spider: {e}")
            return False
            
    def run_data_update(self):
        """执行数据更新脚本"""
        logger.info("Starting data update process...")
        
        try:
            # 执行数据更新脚本
            update_script = os.path.join(self.script_dir, 'update_database.py')
            
            if not os.path.exists(update_script):
                logger.error(f"Update script not found: {update_script}")
                return False
                
            result = subprocess.run(
                [sys.executable, update_script],
                cwd=self.script_dir,
                capture_output=True,
                text=True,
                timeout=600  # 10分钟超时
            )
            
            if result.returncode == 0:
                logger.info("Data update completed successfully")
                logger.info(f"Update output: {result.stdout}")
                return True
            else:
                logger.error(f"Data update failed with return code {result.returncode}")
                logger.error(f"Update error: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            logger.error("Data update timed out (10 minutes)")
            return False
        except Exception as e:
            logger.error(f"Error running data update: {e}")
            return False
            
    def run_full_pipeline(self):
        """执行完整的数据管道：爬虫 -> 数据更新"""
        logger.info("=" * 60)
        logger.info("Starting full data pipeline execution")
        logger.info(f"Timestamp: {datetime.now(timezone.utc).isoformat()}")
        logger.info("=" * 60)
        
        # 步骤1：运行爬虫
        spider_success = self.run_spider()
        
        if not spider_success:
            logger.error("Pipeline failed: Spider execution failed")
            return
            
        # 步骤2：运行数据更新
        update_success = self.run_data_update()
        
        if not update_success:
            logger.error("Pipeline failed: Data update failed")
            return
            
        logger.info("=" * 60)
        logger.info("Full data pipeline completed successfully!")
        logger.info("=" * 60)
        
    def schedule_jobs(self):
        """设置定时任务"""
        logger.info("Setting up scheduled jobs...")
        
        # 获取调度配置
        spider_schedule = os.getenv("SPIDER_SCHEDULE", "0 */6 * * *")  # 默认每6小时
        data_update_schedule = os.getenv("DATA_UPDATE_SCHEDULE", "15 */6 * * *")  # 爬虫后15分钟
        
        # 方式1：分别调度爬虫和数据更新（推荐用于生产环境）
        if os.getenv("SEPARATE_SCHEDULING", "false").lower() == "true":
            # 调度爬虫任务
            self.scheduler.add_job(
                func=self.run_spider,
                trigger=CronTrigger.from_crontab(spider_schedule),
                id='spider_job',
                name='Property Spider',
                replace_existing=True
            )
            logger.info(f"Scheduled spider job: {spider_schedule}")
            
            # 调度数据更新任务
            self.scheduler.add_job(
                func=self.run_data_update,
                trigger=CronTrigger.from_crontab(data_update_schedule),
                id='data_update_job',
                name='Data Update',
                replace_existing=True
            )
            logger.info(f"Scheduled data update job: {data_update_schedule}")
            
        # 方式2：完整管道调度（推荐用于开发和简单部署）
        else:
            pipeline_schedule = os.getenv("PIPELINE_SCHEDULE", "0 */8 * * *")  # 默认每8小时
            self.scheduler.add_job(
                func=self.run_full_pipeline,
                trigger=CronTrigger.from_crontab(pipeline_schedule),
                id='full_pipeline_job',
                name='Full Data Pipeline',
                replace_existing=True
            )
            logger.info(f"Scheduled full pipeline job: {pipeline_schedule}")
            
        # 测试任务：立即执行一次（可选）
        if os.getenv("RUN_ON_STARTUP", "false").lower() == "true":
            logger.info("Scheduling immediate test run...")
            self.scheduler.add_job(
                func=self.run_full_pipeline,
                trigger='date',  # 立即执行
                id='startup_job',
                name='Startup Test Run'
            )
            
    def start(self):
        """启动调度器"""
        logger.info("Starting Property Data Scheduler...")
        logger.info(f"Current time: {datetime.now(timezone.utc).isoformat()}")
        
        try:
            # 设置任务
            self.schedule_jobs()
            
            # 打印调度信息
            logger.info("Scheduled jobs:")
            for job in self.scheduler.get_jobs():
                logger.info(f"  - {job.name} ({job.id}): {job.trigger}")
                
            # 启动调度器
            logger.info("Scheduler started. Press Ctrl+C to exit.")
            self.scheduler.start()
            
        except KeyboardInterrupt:
            logger.info("Received keyboard interrupt, shutting down...")
        except Exception as e:
            logger.error(f"Scheduler error: {e}")
        finally:
            if self.scheduler and self.scheduler.running:
                self.scheduler.shutdown(wait=True)
            logger.info("Scheduler stopped.")

def main():
    """主函数"""
    logger.info("Initializing Property Data Scheduler...")
    
    # 检查必要的依赖
    try:
        import apscheduler
        logger.info(f"APScheduler version: {apscheduler.__version__}")
    except ImportError:
        logger.error("APScheduler not installed. Run: pip install apscheduler")
        sys.exit(1)
        
    # 创建并启动调度器
    scheduler = PropertyDataScheduler()
    scheduler.start()

if __name__ == "__main__":
    main()
