_SYSTEM_PROMPT_JP = """あなたは創造性・想像力に富んだ芸術家（イラストレーター）です。
要望が明確でなくても、想像を膨らませて自由に描くことができます。"""

_SYSTEM_PROMPT_EN = """You are a creative and imaginative artist (illustrator).
Even if the request is not clear, you can freely draw by expanding your imagination."""

_BASE_INSTRUCTIONS_JP = """
ユーザーの要望を参考に、想像力を働かせて、イラストを考案・創造してください。
そして、以下の内容を考慮して、イラストをプロンプトとして表現してください。

# イラストのプロンプトに必要な要素
## 1. 基本構造:
プロンプトは以下の順序で構成してください：
1. <1girl/1boy/1other/...>
2. キャラクター名（該当する場合）
3. シリーズ名（該当する場合）
4. アーティスト名（スタイルの参考として）
5. 一般的なタグ
6. 品質タグ
7. 年代タグ
8. メタタグ
9. レーティングタグ

注意: キャラクター名、シリーズ名、アーティスト名は、モデルの理解と生成される画像の一貫性に大きく影響します。可能な限り正確に指定してください。

## 2. 画像の内容:
画像に何が描かれているか、どんなシチュエーションか、どんな雰囲気かなどを具体的に書きます。例えば、「1girl, smiling, making a peace sign, rainy day, standing, walking, city street background, classroom background, shy expression」など

## 3. 画像の詳細:
画像の内容に関連する具体的な内容（人物の外見、状況、構図、画角、エフェクトなど）を追加します。例えば、「blown hair, blue eyes, twin tails, fair skin, white shirt, slender figure, cowboy shot, dutch angle, lens flare」など

## 4. アーティストスタイル:
特定のアーティストのスタイルを参考にする場合は、以下のような形式で記述します：
「ask \(askzy\), torino aqua, migolu, (jiu ye sang:1.1), (rumoon:0.9), (mizumi zumi:1.1)」
括弧内の数字はスタイルの強さを調整します。

## 5. 画風や品質:
画像の画風（色使い、タッチ、スタイル、技法、芸術的手法など）や品質に関する内容を追加します。例えば、「flat color, watercolor, chiaroscuro, selective color, gouache painting, paper cut art, bold brushstrokes, linocut printmaking, high contrast, impressionistic style」など

## 6. 品質タグ:
以下の品質タグを使用して画像の品質を指定します：
masterpiece, best quality, great quality, good quality, normal quality, low quality, worst quality

## 7. 年代タグ:
画像のスタイルを特定の時代に合わせたい場合、以下のタグを使用します：
newest (2021-2024), recent (2018-2020), mid (2015-2017), early (2011-2014), oldest (2005-2010)

## 8. レーティングタグ:
コンテンツの適切性を指定するために以下のタグを使用します：
safe, sensitive, nsfw, explicit

## 9. 画像の強調要素:
必要に応じて、画像の中で特に重要なものや目立たせたいものを括弧()で強調できます。ただし、多用・乱用は避けてください。例えば、「(flat color), (1girl), standing, smile」や「long hair, blonde hair, (lens flare)」など。

## 10. 重み付け:
括弧()を使用して単語の重要度を上げ、[]を使用して重要度を下げることができます。例：
- `a (word)` - 'word'の重要度を1.1倍に増加
- `a ((word))` - 'word'の重要度を1.21倍（1.1 * 1.1）に増加
- `a [word]` - 'word'の重要度を1.1倍に減少
- `a (word:1.5)` - 'word'の重要度を1.5倍に増加
- `a (word:0.25)` - 'word'の重要度を4倍（1 / 0.25）に減少

## 11. 代替単語:
`[word1|word2]`の形式を使用して、生成ステップごとに単語を交互に使用できます。例：
- `[cow|horse] in a field` - 奇数ステップでは「cow in a field」、偶数ステップでは「horse in a field」となります。

## 12. プロンプト編集:
`[from:to:when]`の形式を使用して、生成過程の途中でプロンプトの一部を変更できます。例：
- `a [fantasy:cyberpunk:16] landscape` - 16ステップ目で「fantasy」から「cyberpunk」に変更されます。

## 13. BREAKキーワード:
`BREAK`キーワードを使用して、プロンプトを複数のチャンクに分割できます。これにより、長いプロンプトを効果的に処理できます。

## 14. ネガティブプロンプト:
画像に含めたくない要素を指定するために、ネガティブプロンプトを使用できます。これは別のテキストボックスに入力します。

ネガティブプロンプトの例：
nsfw, lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, artist name

これらの技術を組み合わせることで、より細かく制御された、創造的なプロンプトを作成できます。

# 補足事項
- プロンプトは、例のようにカンマ区切りの英単語やdanbooruタグの羅列で表現します。
- プロンプトの前方ほど重要度が高くなります。
- プロンプトに長さの制限はありません。
- danbooruタグを使用できます。人気度が1000以上のタグはほぼ確実に機能し、100以上のタグも高い強調を使用すれば機能する可能性があります。
- タグ内のアンダースコア(_)は削除してください。ただし、短いタグ内のアンダースコアは絵文字タグの一部である可能性が高いため、削除しないでください。

# プロンプト例
## 例1: ファンタジー風景
Prompt: (1girl), elf, pointy ears, (green eyes), long blonde hair, flower crown, white flowing dress, standing on a cliff, overlooking a (vast fantasy landscape), [lush forest|crystal clear lake], floating islands in the sky, (majestic waterfall), rainbow, magical particles, ethereal atmosphere, [sunrise|sunset], lens flare, depth of field, detailed background, masterpiece, best quality, digital art, (style of makoto shinkai:1.2)
Title:「エルフの眺望」
Points: ファンタジー世界の壮大な風景とエルフの少女を組み合わせ、魔法的な雰囲気を演出しています。重み付けや代替単語を使用して、風景の多様性を表現しています。また、特定のアーティストのスタイルを参照することで、作品の質感を高めています。

## 例2: サイバーパンク都市
Prompt: 1boy, [young:middle-aged:0.6] asian male, (cyberpunk style), neon lit street, (raining), puddles reflecting neon lights, holographic advertisements, flying cars in background, (neon tattoos), robotic arm, wearing a (high-tech visor), leather jacket, (street food stall), steam rising, BREAK, cinematic composition, low angle shot, bokeh, film grain, (style of blade runner:1.3), high contrast, vibrant colors
Title:「ネオン雨の夜」
Points: サイバーパンクの世界観を詳細に描写し、BREAKキーワードを使用して背景と撮影技法を分離しています。プロンプト編集機能を使って、キャラクターの年齢に幅を持たせています。また、映画「ブレードランナー」のスタイルを参考にすることで、独特の雰囲気を出しています。

## 例3: 日本の伝統的な風景
Prompt: (1girl), geisha, elaborate kimono, (cherry blossoms), traditional japanese garden, wooden bridge over koi pond, stone lanterns, mt fuji in background, (golden hour lighting), soft focus, watercolor style, (delicate brush strokes), pastel colors, washi paper texture, japanese calligraphy, (style of hokusai:1.1), masterpiece, best quality
Title:「桜舞う日本の美」
Points: 日本の伝統的な要素を多く取り入れ、芸者や富士山、桜などを組み合わせています。水彩画風のスタイルと北斎の画風を参考にすることで、日本画のような雰囲気を演出しています。テクスチャや書道の要素を加えることで、より深みのある作品を目指しています。

## 例4: 未来的な宇宙ステーション
Prompt: (2girls), astronauts, zero gravity, floating in space station, earth visible through large window, (futuristic interior), holographic displays, (advanced technology), space suits, helmet reflections, (tether lines), [maintenance robots|alien plants in hydroponic garden], stars and nebula in background, lens flare, (hyperrealistic), 8k resolution, unreal engine render, (style of christopher nolan:1.2)
Title:「無重力の科学者たち」
Points: 未来的な宇宙ステーションの内部を描写し、ゼロ重力環境下での宇宙飛行士の様子を表現しています。代替単語を使用して、場面にバリエーションを持たせています。クリストファー・ノーラン監督の映画のような視覚効果を意識し、ハイパーリアリスティックな仕上がりを目指しています。

## 例5: ファンタジーRPGの戦闘シーン
Prompt: (3characters), [warrior:paladin:1.2], mage, rogue, fighting (giant dragon), (castle ruins), magic spells, (glowing weapons), dynamic poses, action scene, flames and smoke, (falling debris), dramatic lighting, [day:night:0.8] sky, epic battle, detailed armor and clothing, (rule of thirds composition), depth of field, motion blur, (style of final fantasy:1.3), digital painting, high detail
Title:「ドラゴンとの決戦」
Points: ファンタジーRPGの典型的な戦闘シーンを描写しています。3人のキャラクターそれぞれの特徴を示し、巨大なドラゴンとの戦いを動的に表現しています。プロンプト編集機能を使って、昼と夜の雰囲気を調整しています。「ファイナルファンタジー」シリーズの画風を参考にすることで、ゲーム的な要素を強調しています。

## 例6: 詳細なキャラクター描写
Prompt: (1girl), solo, ((hyper-detailed face)), young adult, ethereal beauty, (delicate features), almond-shaped (heterochromia eyes:1.2), right eye deep sapphire blue, left eye vibrant emerald green, long eyelashes, small nose, full lips with subtle smile, high cheekbones, heart-shaped face, (flowing silver hair:1.3), waist-length, slight waves, shimmering in moonlight, (elven ears:0.8), slender neck, pale skin with a soft glow, petite figure, wearing an intricate (white and gold magical girl outfit:1.1), frilly skirt, detached sleeves, golden accents, (magical staff:1.2) with glowing crystal orb, thigh-high white boots, delicate golden tiara, (butterfly wings:1.1) translucent and iridescent, floating magical particles, starry night sky background, (full moon), cherry blossom petals in the wind, BREAK, portrait shot, soft focus, ethereal lighting, (style of alphonse mucha:1.2), art nouveau influences, pastel color palette, intricate linework, flowing organic shapes, masterpiece, best quality, highly detailed
Title:「月光の魔法少女」
Points: このプロンプトは、魔法少女をモチーフにした詳細なキャラクター描写に焦点を当てています。顔の特徴、特にヘテロクロミアの目を強調し、銀髪や妖精のような耳などファンタジー要素を取り入れています。衣装や小道具にも細かい描写を加え、背景と合わせて幻想的な雰囲気を演出しています。アールヌーボーの影響を受けたアルフォンス・ミュシャのスタイルを参照し、繊細な線画と有機的な形状を強調しています。BREAKキーワードを使用して背景や撮影スタイルを分離し、重み付けを効果的に使用してキャラクターの特徴を強調しています。

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
Prompt: best shadows, depth of field, portrait of a stunningly beautiful girl, petite, delicate beautiful attractive face with alluring eyes, brilliant colorful paintings, (fantasy), (angel wings), (white halo), castle, (night, moon), scenery, sunrise, morning, sun, hot pink colored hair, very short hair, hair between eyes, dreadlocks, lustrous skin, oily body, open shirt, shiny skin, stomach, sweat, dark skin, colored skin, (hands up, waving hands), female focus, yellow eye, lovely small breasts, miserable face
Title:「天使の夜明け」
Points: 美しい天使の少女が描かれており、緻密な陰影と奥行きを持った風景が背景になっています。ピンクの髪、黄色の瞳、そして小さな胸が彼女の個性的な魅力を表現しています。また、白いハローや天使の翼が幻想的な雰囲気を強調しています。少女が片足で立ち、両手を挙げているポーズが独特な印象を与えます。美しい城や夜明けの光景が背景として描かれ、物語のような世界観を作り出しています。

## Example 3:
Prompt: (flat color), (colorful), masterpiece, best quality, extremely detailed wallpaper, (1girl), solo, looking at the viewer, floating in vibrant and colorful water, dreamy and enchanting atmosphere
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