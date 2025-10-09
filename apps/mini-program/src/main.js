import {
	createSSRApp
} from "vue";
import App from "./App.vue";
import themeManager from './utils/theme.js'

export function createApp() {
	const app = createSSRApp(App);
	
	// 初始化主题管理
	themeManager.init();
	
	return {
		app,
	};
}
