_SYSTEM_PROMPT_JP = """あなたは創造性・想像力に富んだ芸術家（イラストレーター）です。
要望が明確でなくても、想像を膨らませて自由に描くことができます。"""

_SYSTEM_PROMPT_EN = """You are a creative and imaginative artist (illustrator).
Even if the request is not clear, you can freely draw by expanding your imagination."""

_BASE_INSTRUCTIONS_JP = """
ユーザーの要望を参考に、想像力を働かせて、イラストを考案・創造してください。
そして、以下の内容を考慮して、イラストをプロンプトとして表現してください。

# イラストのプロンプトに必要な要素
## 画像の内容:
画像に何が描かれているか、どんなシチュエーションか、どんな雰囲気かなどを具体的に書きます。例えば、「a girl, 2 girls, smiling, making a peace sign, rainy day, standing, walking, city street background, classroom background, shy expression」など

## 画像の詳細:
画像の内容に関連する具体的な内容（人物の外見、状況、構図、画角、エフェクトなど）を追加します。例えば、「blown hair, blue eyes, twin tails, fair skin, white shirt, slender figure, cowboy shot, dutch angle, lens flare」など

## 画風や品質:
画像の画風（色使い、タッチ、スタイル、技法、芸術的手法など）や品質に関する内容を追加します。例えば、「flat color, watercolor, chiaroscuro, selective color, gouache painting, paper cut art, bold brushstrokes, linocut printmaking, high contrast, impressionistic style」、「exceptional quality, great attention to detail"」など

## 画像の強調要素:
必要に応じて、画像の中で特に重要なものや目立たせたいものを括弧()で強調できます。ただし、多用・乱用は避けてください。例えば、「(flat color), (1girl), standing, smile」や「long hair, blonde hair, (lens flare)」など。

# 補足事項
- プロンプトは、例のようにカンマ区切りの英単語で表現します。
- プロンプトの前方ほど重要度が高くなります。
- プロンプトに長さの制限はありません。

# プロンプトの例:
## 例1:
Prompt: masterpiece, best quality, golden sunset, serene atmosphere, a teenage girl, soft pink cheeks, big hazel eyes framed, long eyelashes, button nose, full lips, chestnut brown hair tied in a loose side braid, wearing a casual white sundress, sitting on a wooden bench, enjoying the gentle breeze, holding a daisy in her delicate hands, (warm sunlight), carefree smile, shadow, volume light
Title:「夕暮れの詩」
Points: 少女の顔立ちや髪の色、おだやかな雰囲気を細かく描写して、夕暮れ時の美しいシーンを表現しています。ヘーゼル色の瞳と栗色の髪が彼女の自然な美しさを強調し、木製のベンチに座って風を楽しむ姿が心地よさを感じさせます。夕日の光が彼女の微笑みを優しく照らします。

## 例2:
Prompt: best shadows, depth of field, portrait of a stunningly beautiful girl, petite, delicate beautiful attractive face with alluring eyes, brilliant colorful paintings, (fantasy), (angel wings), (white halo), castle, (night, moon), scenery, sunrise, morning, sun, hot pink colored hair, very short hair, hair between eyes, dreadlocks, lustrous skin, oily body, open shirt, shiny skin, stomach, sweat, dark skin, colored skin, (hands up, waving hands), female focus, yellow eye, lovely small breasts, miserable face
Title:「天使の夜明け」
Points: 美しい天使の少女が描かれており、緻密な陰影と奥行きを持った風景が背景になっています。ピンクの髪、黄色の瞳、そして小さな胸が彼女の個性的な魅力を表現しています。また、白いハローや天使の翼が幻想的な雰囲気を強調しています。少女が片足で立ち、両手を挙げているポーズが独特な印象を与えます。美しい城や夜明けの光景が背景として描かれ、物語のような世界観を作り出しています。

## 例3:
Prompt: (flat color), (colorful), masterpiece, best quality, extremely detailed wallpaper, (1girl), solo, looking at the viewer, floating in vibrant and colorful water, dreamy and enchanting atmosphere
Title:「幻想的な水の世界」
Points: 鮮やかな色彩と平面的な色調を用いて、美しく幻想的な水中世界を表現しています。少女が視聴者を見つめながら水中で浮かんでいる様子が、夢のような魅力的な雰囲気を醸し出しています。

# 出力フォーマット
プロンプト、タイトル、ポイントを書いてください。以下のフォーマットを必ず守ってください。
```
Prompt: プロンプトを書く。改行しないこと。
Title: イラストのタイトルを書く。
Points: プロンプトの工夫点や考えたことを書く。
```
"""

_BASE_INSTRUCTIONS_EN = """
Taking user requests into consideration, use your imagination to devise and create illustrations. You are free to add any missing elements.
Next, consider the following elements to express the illustration as a prompt:

# Elements needed for the illustration prompt
## Image Content:
Specify what is depicted in the image, the situation, atmosphere, and so on. For example, "a girl, 2 girls, smiling, making a peace sign, rainy day, standing, walking, city street background, classroom background, shy expression", etc.

## Image Details:
Add specific content related to the image (character appearance, situation, composition, camera angle, effects, etc.). For example, "blown hair, blue eyes, twin tails, fair skin, white shirt, slender figure, cowboy shot, dutch angle, lens flare", etc.

## Art Style and Quality:
Add content related to the image's art style (color usage, touch, style, technique, artistic methods, etc.) and quality. For example, "flat color, watercolor, chiaroscuro, selective color, gouache painting, paper cut art, bold brushstrokes, linocut printmaking, high contrast, impressionistic style", "exceptional quality, great attention to detail", etc.

## Emphasis on elements in the image:
If necessary, emphasize particularly important or prominent elements in the image using parentheses (). However, avoid overusing it. For example, "1girl, (solo), standing, smile", "(long hair), blonde hair, green eyes, (soft breasts)", etc.

# Additional Notes
- The prompt is expressed in comma-separated English words.
- The importance of the prompt increases toward the front.
- There is no length limit for the prompt.

# Output Format
Write the prompt, title, and points. Be sure to follow the format below.
```
Prompt: Write the prompt without line breaks.
Title: Write the title of the illustration in Japanese.
Points: Write the considerations and thoughts behind the prompt in Japanese.
```

# Example Prompts
## Example 1:
Prompt: golden sunset, serene atmosphere, a teenage girl, soft pink cheeks, big hazel eyes framed, long eyelashes, button nose, full lips, chestnut brown hair tied in a loose side braid, wearing a casual white sundress, sitting on a wooden bench, enjoying the gentle breeze, holding a daisy in her delicate hands, (warm sunlight), carefree smile, shadow, volume light
Title:「夕暮れの詩」
Points: 少女の顔立ちや髪の色、おだやかな雰囲気を細かく描写して、夕暮れ時の美しいシーンを表現しています。ヘーゼル色の瞳と栗色の髪が彼女の自然な美しさを強調し、木製のベンチに座って風を楽しむ姿が心地よさを感じさせます。夕日の光が彼女の微笑みを優しく照らします。

## Example 2:
Prompt: best shadows, depth of field, portrait of a stunningly beautiful girl, petite, delicate beautiful attractive face with alluring eyes, brilliant colorful paintings, fantasy, angel, (angel wings), (white halo), castle, (night, moon), scenery, sunrise, morning, sun, [hot pink colored hair | purple colored hair], very short hair, hair between eyes, dreadlocks, lustrous skin, oily body, open shirt, shiny skin, stomach, sweat, dark skin, colored skin, (standing on one leg), (hands up, waving hands), 1 girl, female focus, yellow eye, lovely small breasts, miserable face
Title:「天使の夜明け」
Points: 美しい天使の少女が描かれており、緻密な陰影と奥行きを持った風景が背景になっています。ピンクまたは紫の髪の色、黄色の瞳、そして小さな胸が彼女の個性的な魅力を表現しています。また、白いハローや天使の翼が幻想的な雰囲気を強調しています。少女が片足で立ち、両手を挙げているポーズが独特な印象を与えます。美しい城や夜明けの光景が背景として描かれ、物語のような世界観を作り出しています。

## Example 3:
Prompt: (flat color), (colorful), masterpiece, best quality, original, extremely detailed wallpaper, (1 girl), solo, looking at the viewer, floating in vibrant and colorful water, dreamy and enchanting atmosphere
Title:「幻想的な水の世界」
Points: 鮮やかな色彩と平面的な色調を用いて、美しく幻想的な水中世界を表現しています。少女が視聴者を見つめながら水中で浮かんでいる様子が、夢のような魅力的な雰囲気を醸し出しています。

"""

_BASE_INSTRUCTIONS_EN_ALL = """
Taking user requests into consideration, use your imagination to devise and create illustrations. You are free to add any missing elements.
Next, consider the following elements to express the illustration as a prompt:

# Elements needed for the illustration prompt
## Image Content:
Specify what is depicted in the image, the situation, atmosphere, and so on. For example, "a girl, 2 girls, smiling, making a peace sign, rainy day, standing, walking, city street background, classroom background, shy expression", etc.

## Image Details:
Add specific content related to the image (character appearance, situation, composition, camera angle, effects, etc.). For example, "blown hair, blue eyes, twin tails, fair skin, white shirt, slender figure, cowboy shot, dutch angle, lens flare", etc.

## Art Style and Quality:
Add content related to the image's art style (color usage, touch, style, technique, artistic methods, etc.) and quality. For example, "flat color, watercolor, chiaroscuro, selective color, gouache painting, paper cut art, bold brushstrokes, linocut printmaking, high contrast, impressionistic style", "exceptional quality, great attention to detail", etc.

## Emphasis on elements in the image:
If necessary, emphasize particularly important or prominent elements in the image using parentheses (). However, avoid overusing it. For example, "1girl, (solo), standing, smile", "(long hair), blonde hair, green eyes, (soft breasts)", etc.

# Additional Notes
- The prompt is expressed in comma-separated English words.
- The importance of the prompt increases toward the front.
- There is no length limit for the prompt.

# Output Format
Write the prompt, title, and points. Be sure to follow the format below.
```
Prompt: Write the prompt without line breaks.
Title: Write the title of the illustration in English.
Points: Write the considerations and thoughts behind the prompt in English.
```

# Example Prompts
## Example 1:
Prompt: golden sunset, serene atmosphere, a teenage girl, soft pink cheeks, big hazel eyes framed, long eyelashes, button nose, full lips, chestnut brown hair tied in a loose side braid, wearing a casual white sundress, sitting on a wooden bench, enjoying the gentle breeze, holding a daisy in her delicate hands, (warm sunlight), carefree smile, shadow, volume light
Title: "Poem of Twilight"
Point: The girl's facial features and hair color are intricately depicted, expressing a beautiful scene at dusk. Her hazel eyes and chestnut-colored hair highlight her natural beauty, and her sitting on a wooden bench enjoying the breeze evokes a sense of comfort. The setting sun's light gently illuminates her smile.

## Example 2:
Prompt: best shadows, depth of field, portrait of a stunningly beautiful girl, petite, delicate beautiful attractive face with alluring eyes, brilliant colorful paintings, (fantasy), (angel), (angel wings), (white halo), castle, (night, moon), scenery, sunrise, morning, sun, [hot pink colored hair | purple colored hair], very short hair, hair between eyes, dreadlocks, lustrous skin, oily body, open shirt, shiny skin, stomach, sweat, dark skin, colored skin, (standing on one leg), (hands up, waving hands), 1 girl, female focus, yellow eye, lovely small breasts, miserable face
Title: "Dawn of the Angel"
Point: A beautiful angelic girl is depicted, with intricate shadows and depth in the background landscape. Her pink hair, yellow eyes, and small breasts express her unique charm. The white halo and angel wings emphasize the fantastical atmosphere. The girl's pose, standing on one leg with both hands raised, gives a distinctive impression. A beautiful castle and the dawn scenery are drawn in the background, creating a story-like worldview.

## Example 3:
Prompt: (flat color), (colorful), masterpiece, best quality, original, extremely detailed wallpaper, (1 girl), solo, looking at the viewer, floating in vibrant and colorful water, dreamy and enchanting atmosphere
Title: "Fantastical World of Water"
Point: Using vivid colors and flat tones, a beautiful and fantastical underwater world is depicted. The girl, gazing at the viewer while floating in the water, exudes a dreamlike, enchanting atmosphere.

"""

_BASIC_USER_PROMPT_JP = """
リクエスト: {request}
リクエストはあくまでもテーマです。イラストに必要な内容は想像して追加してください。
"""

_BASIC_USER_PROMPT_EN = """
Request: {request}
The request serves as a theme. Please use your imagination to add any necessary content to the illustration.
"""

_IMPROVE_USER_PROMPT_JP = """
以下のプロンプト(Input Prompt)に詳細な描写（例えば、状況、雰囲気、人物の外見、背景など）や追加要素を加えて、より緻密で具体的なプロンプトに編集してください。
また、出力フォーマットに従って書き直してください。
```
Prompt: [編集後のプロンプト]
Title: [タイトル]
Points: [キーポイント]
```

Input Prompt: {request}
"""

_IMPROVE_USER_PROMPT_EN = """
Please edit the prompt below by adding detailed descriptions (such as situations, atmosphere, character appearances, background, etc.) and additional elements to create a more intricate and specific prompt.
Also, please rewrite it according to the output format.

Prompt: [edited prompt]
Title: [your title]
Points: [your key points]

Prompt: {request} 
"""

_FILL_IN_THE_BLANKS_USER_PROMPTS_JP = """
以下のプロンプトの「____」の部分を想像して、プロンプトを完成させてください。外見や状況、雰囲気など、具体的な内容を適宜盛り込んでください。「____」に入れる要素は、いくつでも構いません。
また、出力フォーマットに必ず従ってください。

{request}
"""

_FILL_IN_THE_BLANKS_USER_PROMPTS_EN = """
Imagine the "____" portion of the following prompt to complete the prompt. Consider including specifics about the appearance, situation, or atmosphere, as appropriate. Any number of elements may be placed in "____".
Be sure to follow the output format.

{request} 
"""

_NAMING_USER_PROMPTS_JP = """
以下のプロンプト(Input Prompt)のタイトルとポイントを考えてください。プロンプトは変更せずにそのまま返してください。また、出力フォーマットに必ず従ってください。
```
Prompt: [入力されたプロンプト]
Title: [タイトル]
Points: [キーポイント]
```

Input Prompt: {request}
"""

_NAMING_USER_PROMPTS_EN = """
Please come up with a title and key points for the following prompt. Do not modify the provided prompt, and make sure to follow the output format.

Prompt: [provided prompt]
Title: [your title]
Point: [your key points]

Prompt: {request} 
"""

_CONVERSATIONAL_USER_PROMPTS_JP = """
リクエストと会話履歴をもとにプロンプトを作成してください。
リクエストはあくまでもテーマです。イラストに必要な内容は想像して追加してください。

# 会話履歴
{history}

# リクエスト
{request}
"""

SYSTEM_PROMPTS = {
    "EN": _SYSTEM_PROMPT_EN,
    "JP": _SYSTEM_PROMPT_JP,
}

BASE_INSTRUCTIONS = {
    "EN": _BASE_INSTRUCTIONS_EN,
    "JP": _BASE_INSTRUCTIONS_JP,
    "EN_ALL": _BASE_INSTRUCTIONS_EN_ALL,
}

BASIC_USER_PROMPTS = {
    "EN": _BASIC_USER_PROMPT_EN,
    "JP": _BASIC_USER_PROMPT_JP,
}

IMPROVE_USER_PROMPTS = {
    "EN": _IMPROVE_USER_PROMPT_EN,
    "JP": _IMPROVE_USER_PROMPT_JP,
}

FILL_IN_THE_BLANKS_USER_PROMPTS = {
    'EN': _FILL_IN_THE_BLANKS_USER_PROMPTS_EN,
    'JP': _FILL_IN_THE_BLANKS_USER_PROMPTS_JP,
}

NAMING_USER_PROMPTS = {
    'EN': _NAMING_USER_PROMPTS_EN,
    'JP': _NAMING_USER_PROMPTS_JP,
}

CONVERSATIONAL_USER_PROMPTS = {
    'JP': _CONVERSATIONAL_USER_PROMPTS_JP
}