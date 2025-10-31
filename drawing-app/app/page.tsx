import DrawingCanvas from "@/components/drawing-canvas"

export default function Home() {
  return (
    <>
      <div className="min-h-screen bg-gradient-to-b from-background to-background/80 py-8 px-4">
        <div className="max-w-7xl mx-auto space-y-8">
          <div className="text-center space-y-3">
            <h1 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-primary to-purple-500 bg-clip-text text-transparent">
              AI Sketch to Image
            </h1>
            <p className="text-muted-foreground text-lg">
              Transform your drawings into beautiful images with Gemini AI
            </p>
          </div>

          <DrawingCanvas />
        </div>
      </div>

      {/* Footer */}
      <footer className="border-t border-border/50 bg-card/30 backdrop-blur py-6">
        <div className="container mx-auto px-4 text-center space-y-2">
          <p className="text-sm text-muted-foreground">
            This project is part of{" "}
            <span className="font-semibold text-foreground">
              CLOUD TECHNOLOGY INFRASTRUCTURE (1-2025)
            </span>
          </p>
          <p className="text-sm text-muted-foreground">
            School of Information Technology, KMITL
          </p>
          <p className="text-xs text-muted-foreground/70 mt-2">
            Powered by Next.js, AWS Lambda, and Google Gemini AI
          </p>
        </div>
      </footer>
    </>
  )
}
