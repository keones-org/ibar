import { useState } from 'react'
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Textarea } from "@/components/ui/textarea"
import { Button } from "@/components/ui/button"
import { Slider } from "@/components/ui/slider"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Loader2 } from "lucide-react"

interface CompletionResponse {
  text: string;
  model: string;
}

function App() {
  const [mode, setMode] = useState<'completion' | 'fim'>('completion')
  const [loading, setLoading] = useState(false)
  const [model] = useState('deepseek-chat')
  const [temperature, setTemperature] = useState(0.7)
  const [maxTokens, setMaxTokens] = useState(100)
  const [prompt, setPrompt] = useState('')
  const [prefix, setPrefix] = useState('')
  const [suffix, setSuffix] = useState('')
  const [response, setResponse] = useState<CompletionResponse | null>(null)

  const handleSubmit = async () => {
    setLoading(true)
    try {
      const payload = mode === 'completion' 
        ? { model, prompt, temperature, max_tokens: maxTokens }
        : { model, prefix, suffix, temperature, max_tokens: maxTokens }

      const res = await fetch(`${import.meta.env.VITE_API_URL}/api/completions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })
      
      const data = await res.json()
      setResponse(data)
    } catch (error) {
      console.error('Error:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container mx-auto py-8 space-y-8">
      <Card>
        <CardHeader>
          <CardTitle>DeepSeek LLM Playground</CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="space-y-2">
            <Label>Model</Label>
            <Select value={model} disabled>
              <SelectTrigger>
                <SelectValue placeholder="Select model" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="deepseek-chat">deepseek-chat</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <Tabs value={mode} onValueChange={(v) => setMode(v as 'completion' | 'fim')}>
            <TabsList className="grid w-full grid-cols-2">
              <TabsTrigger value="completion">Completion</TabsTrigger>
              <TabsTrigger value="fim">Fill in Middle</TabsTrigger>
            </TabsList>
            <TabsContent value="completion" className="space-y-4">
              <div className="space-y-2">
                <Label>Prompt</Label>
                <Textarea
                  placeholder="Enter your prompt here..."
                  value={prompt}
                  onChange={(e) => setPrompt(e.target.value)}
                  className="min-h-32"
                />
              </div>
            </TabsContent>
            <TabsContent value="fim" className="space-y-4">
              <div className="space-y-2">
                <Label>Prefix</Label>
                <Textarea
                  placeholder="Enter prefix here..."
                  value={prefix}
                  onChange={(e) => setPrefix(e.target.value)}
                  className="min-h-16"
                />
              </div>
              <div className="space-y-2">
                <Label>Suffix</Label>
                <Textarea
                  placeholder="Enter suffix here..."
                  value={suffix}
                  onChange={(e) => setSuffix(e.target.value)}
                  className="min-h-16"
                />
              </div>
            </TabsContent>
          </Tabs>

          <div className="space-y-2">
            <Label>Temperature: {temperature}</Label>
            <Slider
              value={[temperature]}
              onValueChange={([value]) => setTemperature(value)}
              min={0}
              max={1}
              step={0.1}
            />
          </div>

          <div className="space-y-2">
            <Label>Max Tokens</Label>
            <Input
              type="number"
              value={maxTokens}
              onChange={(e) => setMaxTokens(Number(e.target.value))}
              min={1}
              max={2048}
            />
          </div>

          <Button 
            onClick={handleSubmit} 
            className="w-full"
            disabled={loading || (!prompt && !(prefix || suffix))}
          >
            {loading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Generating...
              </>
            ) : (
              'Generate'
            )}
          </Button>
        </CardContent>
      </Card>

      {response && (
        <Card>
          <CardHeader>
            <CardTitle>Response</CardTitle>
          </CardHeader>
          <CardContent>
            <pre className="whitespace-pre-wrap bg-slate-50 p-4 rounded-lg">
              {response.text}
            </pre>
          </CardContent>
        </Card>
      )}
    </div>
  )
}

export default App
