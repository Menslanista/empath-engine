const { toEmotionPredictionObject, toPlayerBehaviorProto } = require('../src/utils/converters.js')

test('toEmotionPredictionObject produces object with fields', () => {
  const obj = toEmotionPredictionObject({ dominantEmotion: 'engaged', confidence: 0.9, timestampMs: 1 })
  expect(obj.dominantEmotion).toBe('engaged')
  expect(obj.confidence).toBeCloseTo(0.9)
})

test('toPlayerBehaviorProto sets fields', () => {
  const pb = toPlayerBehaviorProto({ sessionId: 's', recentChoices: [1,2], decisionLatencyMs: 10 })
  expect(pb.getSessionId()).toBe('s')
  expect(pb.getRecentChoicesList()).toEqual([1,2])
})
