import { EmotionPrediction, PlayerBehaviorData } from '../proto/emotion_pb.js'

export function toEmotionPredictionObject({ dominantEmotion, confidence, timestampMs }) {
  const p = new EmotionPrediction()
  if (dominantEmotion) p.setDominantEmotion(dominantEmotion)
  if (confidence != null) p.setConfidence(confidence)
  if (timestampMs != null) p.setTimestampMs(timestampMs)
  return p.toObject()
}

export function toPlayerBehaviorProto(payload) {
  const d = new PlayerBehaviorData()
  if (payload.sessionId) d.setSessionId(payload.sessionId)
  if (payload.timestampMs != null) d.setTimestampMs(payload.timestampMs)
  if (payload.decisionLatencyMs != null) d.setDecisionLatencyMs(payload.decisionLatencyMs)
  if (payload.actionFrequency != null) d.setActionFrequency(payload.actionFrequency)
  if (Array.isArray(payload.recentChoices)) d.setRecentChoicesList(payload.recentChoices)
  return d
}
