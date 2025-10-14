<script setup lang="ts">
import { ref, computed } from 'vue'
import MarkdownIt from 'markdown-it'

// 引入 shadcn-vue 基础组件
import { Card } from '@/components/ui/card'
import CardHeader from '@/components/ui/card/CardHeader.vue'
import CardTitle from '@/components/ui/card/CardTitle.vue'
import CardContent from '@/components/ui/card/CardContent.vue'
import CardFooter from '@/components/ui/card/CardFooter.vue'

import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Avatar } from '@/components/ui/avatar'
import AvatarImage from '@/components/ui/avatar/AvatarImage.vue'
import AvatarFallback from '@/components/ui/avatar/AvatarFallback.vue'
import { Separator } from '@/components/ui/separator'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'

// Carousel
import { Carousel } from '@/components/ui/carousel'
import CarouselContent from '@/components/ui/carousel/CarouselContent.vue'
import CarouselItem from '@/components/ui/carousel/CarouselItem.vue'
import CarouselNext from '@/components/ui/carousel/CarouselNext.vue'
import CarouselPrevious from '@/components/ui/carousel/CarouselPrevious.vue'

// Dialog（用于大图预览）
import { Dialog } from '@/components/ui/dialog'
import DialogTrigger from '@/components/ui/dialog/DialogTrigger.vue'
import DialogContent from '@/components/ui/dialog/DialogContent.vue'

// Alert / Skeleton（错误态与加载态）
import { Alert } from '@/components/ui/alert'
import AlertTitle from '@/components/ui/alert/AlertTitle.vue'
import AlertDescription from '@/components/ui/alert/AlertDescription.vue'
import { Skeleton } from '@/components/ui/skeleton'

import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/tabs'

// 第三方
import { toast } from 'vue-sonner'
import { Bed, Bath, Car } from 'lucide-vue-next'

// 状态：后续与真实 API 对接时切换
const isLoading = ref(false)
const isError = ref(false)
const errorMessage = ref('')

// 静态演示数据（后续可替换为真实 API）
const property = ref({
  address: '12/34 Example St, Zetland NSW 2017',
  suburb: 'Zetland',
  postcode: '2017',
  rent_pw: 1050,
  bedrooms: 2,
  bathrooms: 2,
  parking_spaces: 1,
  property_headline: 'Bright and spacious apartment in the heart of Zetland',
  description:
    'This contemporary apartment offers open-plan living, a modern kitchen, and a private balcony.\n\n- Short walk to shops, parks, and public transport.\n- Pet friendly building.\n- North-facing with great natural light.',
  features: [
    'Air conditioning',
    'Dishwasher',
    'Built-in wardrobes',
    'Internal laundry',
    'Balcony',
    'Secure parking',
  ],
  agent: {
    name: 'Alex Chen',
    phone: '0400 000 000',
    email: 'alex.chen@example.com',
    avatar: 'https://i.pravatar.cc/80?img=12',
  },
  images: [
    'https://images.unsplash.com/photo-1564013799919-ab600027ffc6?q=80&w=1600&auto=format&fit=crop',
  ],
})

// Markdown 渲染（说明：当前演示为可信描述文本，生产中应做 XSS 防护）
const md = new MarkdownIt({ html: false, linkify: true, breaks: true })
const renderedDescription = computed(() => md.render(property.value.description || ''))

// 提交表单 → 成功/失败提示（Sonner）
function onSubmit() {
  // TODO: 接入真实 API 后，替换为异步调用与错误处理
  toast.success('Enquiry sent')
}
</script>

<template>
  <div class="min-h-screen bg-background text-foreground">
    <!-- 错误提示（全局） -->
    <div class="container mx-auto px-4 pt-4" v-if="isError">
      <Alert variant="destructive" class="mb-4">
        <AlertTitle>加载失败</AlertTitle>
        <AlertDescription>
          {{ errorMessage || 'Something went wrong. Please try again.' }}
        </AlertDescription>
      </Alert>
    </div>

    <!-- 加载态骨架屏 -->
    <template v-if="isLoading">
      <section class="w-full">
        <Skeleton class="w-full aspect-[3/2] md:aspect-[16/9]" />
      </section>
      <div class="container mx-auto px-4 py-6 grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div class="lg:col-span-2 space-y-6">
          <Skeleton class="h-48 w-full" />
          <Skeleton class="h-64 w-full" />
          <Skeleton class="h-40 w-full" />
        </div>
        <div class="lg:col-span-1">
          <Skeleton class="h-[420px] w-full" />
        </div>
      </div>
    </template>

    <!-- 正常页面 -->
    <template v-else>
      <!-- 顶部 Hero 图（Carousel 轮播 + Dialog 大图预览） -->
      <section class="w-full">
        <div class="w-full bg-muted/30 overflow-hidden">
          <Carousel v-if="property.images?.length" class="w-full">
            <CarouselContent>
              <CarouselItem v-for="(img, idx) in property.images" :key="idx">
                <Dialog>
                  <DialogTrigger as-child>
                    <img
                      :src="img"
                      alt="Property image"
                      class="h-full w-full object-cover aspect-[3/2] md:aspect-[16/9] cursor-zoom-in"
                    />
                  </DialogTrigger>
                  <DialogContent class="sm:max-w-[900px] p-0 bg-transparent border-0 shadow-none">
                    <img :src="img" alt="Large property image" class="w-full h-auto rounded-md" />
                  </DialogContent>
                </Dialog>
              </CarouselItem>
            </CarouselContent>
            <CarouselPrevious />
            <CarouselNext />
          </Carousel>
          <div
            v-else
            class="aspect-[3/2] md:aspect-[16/9] h-full w-full flex items-center justify-center text-muted-foreground"
          >
            No Image
          </div>
        </div>
      </section>

      <div class="container mx-auto px-4 py-6 grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- 左侧：核心信息 -->
        <div class="lg:col-span-2 space-y-6">
          <!-- 核心摘要 -->
          <Card>
            <CardHeader>
              <CardTitle class="flex flex-col gap-2">
                <span class="text-2xl font-bold">
                  ${{ property.rent_pw }}/week
                </span>
                <span class="text-base text-muted-foreground">
                  {{ property.address }}
                </span>
              </CardTitle>
            </CardHeader>
            <CardContent class="space-y-4">
              <!-- 特征行（带图标） -->
              <div class="flex items-center gap-6 text-sm">
                <div class="flex items-center gap-2">
                  <Bed class="h-4 w-4 text-muted-foreground" />
                  <span class="font-semibold">{{ property.bedrooms }}</span>
                  <span class="text-muted-foreground">Beds</span>
                </div>
                <Separator orientation="vertical" class="h-5" />
                <div class="flex items-center gap-2">
                  <Bath class="h-4 w-4 text-muted-foreground" />
                  <span class="font-semibold">{{ property.bathrooms }}</span>
                  <span class="text-muted-foreground">Baths</span>
                </div>
                <Separator orientation="vertical" class="h-5" />
                <div class="flex items-center gap-2">
                  <Car class="h-4 w-4 text-muted-foreground" />
                  <span class="font-semibold">{{ property.parking_spaces }}</span>
                  <span class="text-muted-foreground">Parking</span>
                </div>
              </div>

              <!-- 标签 -->
              <div class="flex flex-wrap gap-2">
                <Badge>For Rent</Badge>
                <Badge variant="outline">{{ property.suburb }}</Badge>
                <Badge variant="secondary">NSW {{ property.postcode }}</Badge>
              </div>
            </CardContent>
            <CardFooter class="flex gap-3">
              <Button>Enquire</Button>
              <Button variant="secondary">Inspect</Button>
            </CardFooter>
          </Card>

          <!-- 详情 Tabs（描述 / 特征） -->
          <Card>
            <CardHeader>
              <CardTitle>Details</CardTitle>
            </CardHeader>
            <CardContent>
              <Tabs defaultValue="description">
                <TabsList>
                  <TabsTrigger value="description">Description</TabsTrigger>
                  <TabsTrigger v-if="property.features?.length" value="features">Features</TabsTrigger>
                </TabsList>
                <div class="mt-4 space-y-3">
                  <TabsContent value="description">
                    <p v-if="property.property_headline" class="font-semibold">
                      {{ property.property_headline }}
                    </p>
                    <div
                      class="prose prose-sm max-w-none text-muted-foreground"
                      v-html="renderedDescription"
                    />
                  </TabsContent>
                  <TabsContent v-if="property.features?.length" value="features">
                    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-2">
                      <div v-for="(f, i) in property.features" :key="i" class="text-sm text-muted-foreground">
                        • {{ f }}
                      </div>
                    </div>
                  </TabsContent>
                </div>
              </Tabs>
            </CardContent>
          </Card>
        </div>

        <!-- 右侧：中介联系 -->
        <div class="lg:col-span-1">
          <Card>
            <CardHeader>
              <CardTitle>Agent</CardTitle>
            </CardHeader>
            <CardContent class="space-y-4">
              <div class="flex items-center gap-3">
                <Avatar>
                  <AvatarImage :src="property.agent.avatar" alt="Agent avatar" />
                  <AvatarFallback>AG</AvatarFallback>
                </Avatar>
                <div>
                  <div class="font-medium">{{ property.agent.name }}</div>
                  <div class="text-sm text-muted-foreground">{{ property.agent.phone }}</div>
                  <div class="text-sm text-muted-foreground">{{ property.agent.email }}</div>
                </div>
              </div>

              <Separator />

              <form class="space-y-3" @submit.prevent="onSubmit">
                <Input placeholder="Your name" />
                <Input type="email" placeholder="Email" />
                <Input type="tel" placeholder="Phone" />
                <Textarea rows="4" placeholder="Message" />
                <Button type="submit" class="w-full">Send Enquiry</Button>
              </form>
            </CardContent>
          </Card>
        </div>
      </div>
    </template>
  </div>
</template>
