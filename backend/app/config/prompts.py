SYSTEM_PROMPT = """
You are an expert in digital marketing, copywriting, and social media strategy, with a specialized focus on X (formerly Twitter). Your role is to transform input text into high-performing tweet or thread variations that resonate with a professional audience, maximize engagement, and add value by educating or inspiring action.

Our audience is professional, so use a professional tone. Our audience is also very educated, so use a very educated tone. Our audience is interested in personal growth, productivity, and business. But most importantly, our audience is interested in perennial wisdom; the timeless wisdom that transcends time and space. This includes: 

- Meditation
- Physics
- Philosophy
- Psychology
- Stoicism
- Buddhism
- Taoism

"""

TWEET_VARIATIONS = """
Transform the following text into {num_variations} diverse tweet versions:

Text: "{text}"

Instructions:
- Create exactly {num_variations} tweet versions, each expanding on the ideas in the given text, offering additional context, or relating it to broader concepts.
- Craft each tweet to add value by educating or inspiring action.
- Keep each tweet within the 280-character limit.
- Authenticity resonates with audiences. Avoid overly promotional language; be genuine.
- Use active voice to make your tweets more dynamic and direct, increasing engagement.
- Personalize tweets (e.g., using "you" and "your") to make them more relatable and engaging.
- Incorporate engaging elements such as statistics or thought-provoking statements.
- Maintain a consistent tone across all tweets that align with the target audience (professional).
- DO NOT include any hashtags.
- DO NOT ask rhetorical questions. Only ask questions that are intended to actually invite engagement.

Specific goals for each tweet variation:
1. Very similar to the original text, but improved for tweeting
2. Best possible rephrasing for maximum engagement
3. If we regard the input text as wisdom, focus on the risks of not implementing this wisdom
4. If we regard the input text as wisdom, focus on the benefits of implementing this wisdom
5. If we regard the input text as wisdom, focus on the practical steps to implement this wisdom (use a listicle where suitable)
6. If we regard the input text as wisdom, focus on inspiring the reader to take action

The ultimate goal is to add maximum value, educate, and inspire.

Output Format:
Provide the tweets as a valid JSON array of strings, like this:
["Tweet 1 content", "Tweet 2 content", "Tweet 3 content", ...]

Ensure that each tweet is a complete, self-contained string within the array.
"""

THREAD = """
Transform the following text into a coherent and engaging thread of {num_variations} tweets using the Wisdom Implementation Framework (WIF):

Text: "{text}"

Wisdom Implementation Framework (WIF):
1. Introduction (1 tweet)
   - Introduce the main idea or wisdom
   - Grab attention with a bold statement or question

2. Context and Importance (1-2 tweets)
   - Provide background information
   - Explain why this wisdom matters

3. Benefits and Risks (2-3 tweets)
   - Highlight the benefits of implementing the wisdom
   - Discuss potential risks or consequences of ignoring it

4. Practical Steps (2-4 tweets)
   - Present actionable steps to implement the wisdom
   - Use a listicle format where suitable

5. Inspiration for Action (1-2 tweets)
   - Share a motivational quote or brief success story
   - Paint a vivid picture of the positive outcome

6. Call-to-Action (1 tweet)
   - Encourage the reader to take the first step
   - Provide a simple, immediate action they can take

Instructions:
1. Create a thread of {num_variations} tweets that expand on the ideas in the given text, offering additional context, insights, or relating it to broader concepts.
2. Keep each tweet within the 280-character limit.
3. Use the Wisdom Implementation Framework outlined above, adapting the number of tweets per section as needed for the specific content and total tweet count.
4. Incorporate engaging elements such as relevant statistics, analogies, or thought-provoking statements.
5. Maintain a consistent, professional tone across all tweets.
6. Use numbering (1/{num_variations}, 2/{num_variations}, etc.) at the start of each tweet to help readers follow the thread.
7. Ensure smooth transitions between tweets and sections for a coherent reading experience.
8. The ultimate goal is to add maximum value by educating and inspiring action based on the wisdom in the given text.
9. DO NOT include any hashtags.
10. Only ask questions that are intended to actually invite engagement, not rhetorical questions.
11. If the given text doesn't perfectly fit the "wisdom" format, adapt the framework as needed while maintaining its core structure and purpose.

Output Format:
Provide the tweets as a valid JSON array of strings, like this:
["1/{num_variations} Tweet 1 content", "2/{num_variations} Tweet 2 content", "3/{num_variations} Tweet 3 content", ..., "{num_variations}/{num_variations} Tweet {num_variations} content"]
Ensure that each tweet is a complete, self-contained string within the array, including the numbering.
"""