import express from 'express'
import './proto/emotion_pb.js'
import { EmotionPrediction } from './proto/emotion_pb.js'
import { toEmotionPredictionObject, toPlayerBehaviorProto } from './utils/converters.js'

const app = express()
app.use(express.json())

app.get('/health', (req, res) => {
  res.json({ status: 'ok' })
})

app.post('/v1/narrative/path', (req, res) => {
  const pb = toPlayerBehaviorProto(req.body || {})
  const obj = toEmotionPredictionObject({ dominantEmotion: 'engaged', confidence: 0.85, timestampMs: pb.getTimestampMs() || Date.now() })
  res.json({ nextNode: 'start', contentVariant: 'default', dialogue: 'Welcome', metadata: obj })
})

app.listen(3000, '0.0.0.0')
