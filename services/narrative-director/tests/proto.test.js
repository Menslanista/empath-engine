const { EmotionPrediction } = require('../src/proto/emotion_pb.js')

test('emotion prediction toObject', () => {
  const p = new EmotionPrediction()
  p.setDominantEmotion('engaged')
  p.setConfidence(0.85)
  const obj = p.toObject()
  expect(obj.dominantEmotion).toBe('engaged')
})
