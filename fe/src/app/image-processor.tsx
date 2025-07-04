"use client"

import { useState, useRef, useEffect } from "react"
import Image from "next/image"
import { Slider } from "@/components/ui/slider"
import { Button } from "@/components/ui/button"
import { Checkbox } from "@/components/ui/checkbox"
import { Label } from "@/components/ui/label"
import { UploadIcon, DownloadIcon, GridIcon, ChevronDown } from 'lucide-react'
import * as Collapsible from '@radix-ui/react-collapsible'

export default function ImageProcessor() {
  const [image, setImage] = useState<string | null>(null)
  const [originalImage, setOriginalImage] = useState<string | null>(null)
  const [opacity, setOpacity] = useState(100)
  const [contrast, setContrast] = useState(100)
  const [brightness, setBrightness] = useState(100)
  const [saturation, setSaturation] = useState(100)
  const [blur, setBlur] = useState(0)
  const [hueRotate, setHueRotate] = useState(0)
  const [isInverted, setIsInverted] = useState(false)
  const [isBlackAndWhite, setIsBlackAndWhite] = useState(false)
  const [isSepia, setIsSepia] = useState(false)
  const [isEmboss, setIsEmboss] = useState(false)
  const [downloadUrl, setDownloadUrl] = useState<string | null>(null)
  const [isProcessing, setIsProcessing] = useState(false)
  const [isAdjustmentsOpen, setIsAdjustmentsOpen] = useState(false)
  const [isEffectsOpen, setIsEffectsOpen] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)
  const canvasRef = useRef<HTMLCanvasElement>(null)

  const API_URL = process.env.NEXT_PUBLIC_API_URL;

  const defaultValues = {
    opacity: 100,
    contrast: 100,
    brightness: 100,
    saturation: 100,
    blur: 0,
    hueRotate: 0,
    isInverted: false,
    isBlackAndWhite: false,
    isSepia: false,
    isEmboss: false,
  }

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file) {
      const reader = new FileReader()
      reader.onload = (e) => {
        setImage(e.target?.result as string)
        setOriginalImage(e.target?.result as string)
      }
      reader.readAsDataURL(file)
    }
  }

  const handleSliderChange = (setter: React.Dispatch<React.SetStateAction<number>>) => (value: number[]) => {
    setter(value[0])
  }

  const getImageFilters = () => {
    let filters = [
      `contrast(${contrast}%)`,
      `brightness(${brightness}%)`,
      `saturate(${saturation}%)`,
      `blur(${blur}px)`,
      `hue-rotate(${hueRotate}deg)`
    ]
    if (isInverted) filters.push("invert(100%)")
    if (isBlackAndWhite) filters.push("grayscale(100%)")
    if (isSepia) filters.push("sepia(100%)")
    return filters.join(" ")
  }

  useEffect(() => {
    if (image) {
      const img = document.createElement('img')
      img.onload = () => {
        if (canvasRef.current) {
          const canvas = canvasRef.current
          canvas.width = img.width
          canvas.height = img.height
          const ctx = canvas.getContext('2d')
          if (ctx) {
            ctx.filter = getImageFilters()
            ctx.globalAlpha = opacity / 100
            ctx.drawImage(img, 0, 0, img.width, img.height)
            
            if (isEmboss) {
              const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height)
              const embossedData = embossFilter(imageData)
              ctx.putImageData(embossedData, 0, 0)
            }
            
            setDownloadUrl(canvas.toDataURL())
          }
        }
      }
      img.src = image
    }
  }, [image, opacity, contrast, brightness, saturation, blur, hueRotate, isInverted, isBlackAndWhite, isSepia, isEmboss])

  const embossFilter = (imageData: ImageData) => {
    const width = imageData.width
    const height = imageData.height
    const data = imageData.data
    const outputData = new ImageData(width, height)
    for (let y = 1; y < height - 1; y++) {
      for (let x = 1; x < width - 1; x++) {
        const index = (y * width + x) * 4
        for (let c = 0; c < 3; c++) {
          outputData.data[index + c] = 
            127 + 2 * data[index + c] - 
            data[index - 4 + c] - 
            data[index + 4 + c]
        }
        outputData.data[index + 3] = data[index + 3]
      }
    }
    return outputData
  }

  const handleDownload = () => {
    if (downloadUrl) {
      const link = document.createElement('a')
      link.href = downloadUrl
      link.download = 'adjusted-image.png'
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
    }
  }

  const handleCreateMosaic = async () => {
    if (image) {
      setIsProcessing(true)
      try {
        const response = await fetch(API_URL + '/api/create-mosaic', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ image }),
        })
        if (response.ok) {
          const blob = await response.blob()
          if (blob.type === 'image/jpeg') {
            // Convert blob to base64 string
            const reader = new FileReader()
            reader.onloadend = () => {
              const base64String = reader.result as string
              setImage(base64String)
            }
            reader.readAsDataURL(blob)
          } else {
            console.error('Unexpected response type:', blob.type)
          }
        } else {
          console.error('Failed to create mosaic')
        }
      } catch (error) {
        console.error('Error creating mosaic:', error)
      } finally {
        setIsProcessing(false)
      }
    }
  }

  const handleReset = () => {
    setImage(originalImage)
    setOpacity(defaultValues.opacity)
    setContrast(defaultValues.contrast)
    setBrightness(defaultValues.brightness)
    setSaturation(defaultValues.saturation)
    setBlur(defaultValues.blur)
    setHueRotate(defaultValues.hueRotate)
    setIsInverted(defaultValues.isInverted)
    setIsBlackAndWhite(defaultValues.isBlackAndWhite)
    setIsSepia(defaultValues.isSepia)
    setIsEmboss(defaultValues.isEmboss)
  }

  return (
    <div className="flex flex-col space-y-6 p-6 max-w-2xl mx-auto">
      <h2 className="text-2xl font-bold text-center">Image Processor</h2>
      
      <div className="w-full aspect-square relative bg-white border rounded-lg overflow-hidden">
        {image ? (
          <Image
            src={image}
            alt="Uploaded image"
            fill
            style={{ 
              opacity: opacity / 100,
              filter: getImageFilters()
            }}
            className="object-contain"
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center text-gray-400">
            No image uploaded
          </div>
        )}
      </div>

      <Collapsible.Root 
        className="w-full" 
        open={isAdjustmentsOpen} 
        onOpenChange={setIsAdjustmentsOpen}
      >
        <Collapsible.Trigger asChild>
          <Button variant="outline" className="w-full flex justify-between items-center">
            Image Adjustments
            <ChevronDown className={`h-4 w-4 transition-transform duration-200 ${isAdjustmentsOpen ? 'transform rotate-180' : ''}`} />
          </Button>
        </Collapsible.Trigger>
        <Collapsible.Content className="mt-4 space-y-4">
          {[
            { label: "Opacity", value: opacity, min: 0, max: 100, setter: setOpacity },
            { label: "Contrast", value: contrast, min: 0, max: 200, setter: setContrast },
            { label: "Brightness", value: brightness, min: 0, max: 200, setter: setBrightness },
            { label: "Saturation", value: saturation, min: 0, max: 200, setter: setSaturation },
            { label: "Blur", value: blur, min: 0, max: 10, setter: setBlur },
            { label: "Hue Rotate", value: hueRotate, min: 0, max: 360, setter: setHueRotate },
          ].map((slider) => (
            <div key={slider.label}>
              <Label htmlFor={`${slider.label.toLowerCase().replace(' ', '-')}-slider`}>{slider.label}</Label>
              <Slider
                id={`${slider.label.toLowerCase().replace(' ', '-')}-slider`}
                min={slider.min}
                max={slider.max}
                step={1}
                value={[slider.value]}
                onValueChange={handleSliderChange(slider.setter)}
                aria-label={`Adjust image ${slider.label.toLowerCase()}`}
              />
              <p className="text-sm text-gray-500 mt-1">
                {slider.label}: {slider.value}
                {slider.label === "Blur" ? "px" : slider.label === "Hue Rotate" ? "°" : "%"}
              </p>
            </div>
          ))}
        </Collapsible.Content>
      </Collapsible.Root>

      <Collapsible.Root 
        className="w-full" 
        open={isEffectsOpen} 
        onOpenChange={setIsEffectsOpen}
      >
        <Collapsible.Trigger asChild>
          <Button variant="outline" className="w-full flex justify-between items-center">
            Image Effects
            <ChevronDown className={`h-4 w-4 transition-transform duration-200 ${isEffectsOpen ? 'transform rotate-180' : ''}`} />
          </Button>
        </Collapsible.Trigger>
        <Collapsible.Content className="mt-4 space-y-4">
          {[
            { id: "invert", label: "Invert colors", state: isInverted, setter: setIsInverted },
            { id: "blackAndWhite", label: "Black and white", state: isBlackAndWhite, setter: setIsBlackAndWhite },
            { id: "sepia", label: "Sepia", state: isSepia, setter: setIsSepia },
            { id: "emboss", label: "Emboss", state: isEmboss, setter: setIsEmboss },
          ].map((effect) => (
            <div key={effect.id} className="flex items-center space-x-2">
              <Checkbox 
                id={effect.id} 
                checked={effect.state}
                onCheckedChange={(checked) => effect.setter(checked as boolean)}
              />
              <Label htmlFor={effect.id}>{effect.label}</Label>
            </div>
          ))}
        </Collapsible.Content>
      </Collapsible.Root>

      <div className="w-full flex space-x-4">
        <input
          type="file"
          accept="image/*"
          onChange={handleFileChange}
          ref={fileInputRef}
          className="hidden"
        />
        <Button 
          onClick={() => fileInputRef.current?.click()}
          className="flex-1"
        >
          <UploadIcon className="mr-2 h-4 w-4" /> Upload Image
        </Button>
        <Button 
          onClick={handleDownload}
          className="flex-1"
          disabled={!downloadUrl}
        >
          <DownloadIcon className="mr-2 h-4 w-4" /> Download Adjusted Image
        </Button>
        <Button
          onClick={handleReset}
          className="flex-1"
          variant="outline"
        >
          Reset Adjustments
        </Button>
      </div>

      <div className="w-full">
        <Button
          onClick={handleCreateMosaic}
          className="w-full"
          disabled={!image || isProcessing}
        >
          <GridIcon className="mr-2 h-4 w-4" />
          {isProcessing ? 'Creating Mosaic...' : 'Create Mosaic'}
        </Button>
      </div>

      <canvas ref={canvasRef} className="hidden" />
    </div>
  )
}