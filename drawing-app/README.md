# AI Sketch to Image

Transform your drawings into beautiful images with Gemini AI. A Next.js web application that uses AWS Lambda and Google Gemini to convert hand-drawn sketches into AI-generated images.

![Next.js](https://img.shields.io/badge/Next.js-15-black?logo=next.js)
![TypeScript](https://img.shields.io/badge/TypeScript-5-blue?logo=typescript)
![AWS Lambda](https://img.shields.io/badge/AWS-Lambda-orange?logo=amazon-aws)
![Gemini AI](https://img.shields.io/badge/Google-Gemini-4285F4?logo=google)

## 🎨 Features

- **Interactive Drawing Canvas** - Draw sketches with customizable brush colors and sizes
- **AI Image Generation** - Convert sketches to realistic images using Google Gemini AI
- **Multiple Art Styles** - Choose from realistic, anime, watercolor, and more styles
- **Eraser Tool** - Correct mistakes while drawing
- **Download Support** - Save your drawings and generated images
- **Responsive Design** - Works on desktop and mobile devices
- **Dark Theme** - Modern dark UI with gradient accents

## 🛠️ Tech Stack

### Frontend
- **Next.js 15** - React framework with App Router
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first styling
- **Radix UI** - Accessible UI components
- **Lucide Icons** - Beautiful icon library

### Backend
- **AWS Lambda** - Serverless image generation
- **AWS API Gateway** - REST API endpoint
- **AWS S3** - Image storage (optional)
- **Google Gemini AI** - Image generation model

## 📋 Prerequisites

- Node.js 18+ 
- pnpm (recommended) or npm
- AWS Account (for Lambda deployment)
- Google Gemini API Key

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Whiterose48/AWS.git
cd drawing-app
```

### 2. Install dependencies

```bash
pnpm install
```

### 3. Set up environment variables

Create a `.env.local` file in the root directory:

```env
API_GATEWAY_URL=https://[your-api-id].execute-api.[region].amazonaws.com/prod/generate
```

### 4. Deploy AWS Lambda

Follow the detailed instructions in [AWS_SETUP.md](./AWS_SETUP.md) to:
1. Create the Lambda function
2. Set up API Gateway
3. Configure CORS
4. Add your Gemini API key

### 5. Run the development server

```bash
pnpm dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## 📁 Project Structure

```
drawing-app/
├── app/
│   ├── api/
│   │   └── generate/        # API route for Lambda proxy
│   ├── globals.css          # Global styles
│   ├── layout.tsx           # Root layout
│   └── page.tsx             # Home page
├── components/
│   ├── drawing-canvas.tsx   # Main drawing component
│   ├── theme-provider.tsx   # Dark theme provider
│   └── ui/                  # Reusable UI components
├── hooks/                   # Custom React hooks
├── lib/                     # Utility functions
├── lambda_function.py       # AWS Lambda function code
└── AWS_SETUP.md            # AWS deployment guide
```

## 🎯 How It Works

1. **Draw** - Create a sketch on the canvas using the drawing tools
2. **Select Style** - Choose your preferred art style (realistic, anime, etc.)
3. **Generate** - Click "Generate with AI" to send the sketch to AWS Lambda
4. **View Result** - The AI generates an image based on your sketch
5. **Download** - Save the generated image to your device

## 🔧 Available Scripts

| Command | Description |
|---------|-------------|
| `pnpm dev` | Start development server |
| `pnpm build` | Build for production |
| `pnpm start` | Start production server |
| `pnpm lint` | Run ESLint |

## 🌐 AWS Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐     ┌────────────┐
│   Next.js   │────▶│ API Gateway  │────▶│   Lambda    │────▶│ Gemini AI  │
│   Frontend  │◀────│    (REST)    │◀────│  Function   │◀────│   API      │
└─────────────┘     └──────────────┘     └─────────────┘     └────────────┘
                                                │
                                                ▼
                                         ┌─────────────┐
                                         │   S3 Bucket │
                                         │  (Optional) │
                                         └─────────────┘
```

## 📄 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `API_GATEWAY_URL` | AWS API Gateway endpoint URL | Yes |

### Lambda Environment Variables

| Variable | Description |
|----------|-------------|
| `GEMINI_API_KEY` | Google Gemini API key |
| `S3_BUCKET_NAME` | S3 bucket for image storage |

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License.

## 🎓 Academic Project

This project is part of **CLOUD TECHNOLOGY INFRASTRUCTURE (1-2025)**  
School of Information Technology, KMITL

## Member

Natthawee Naewkampol

Phachara Pornanothai

Yodsakorn Chuwong

Porntipa Phunsri

Asia Onprom
---

<p align="center">
  Powered by Next.js, AWS Lambda, and Google Gemini AI
</p>
