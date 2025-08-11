"""
Comprehensive style presets for image generation
"""

STYLE_PRESETS = {
    "photorealistic": {
        "prefix": "Ultra-realistic photograph,",
        "suffix": "professional photography, sharp focus, high resolution, detailed textures",
        "modifiers": ["8K", "RAW photo", "masterpiece", "award-winning"]
    },
    "cinematic": {
        "prefix": "Cinematic shot,",
        "suffix": "dramatic lighting, film grain, anamorphic lens, movie scene",
        "modifiers": ["35mm film", "Hollywood production", "epic composition"]
    },
    "anime": {
        "prefix": "Anime art style,",
        "suffix": "detailed anime artwork, vibrant colors, manga aesthetic",
        "modifiers": ["studio quality", "trending on pixiv", "by famous anime artist"]
    },
    "ghibli": {
        "prefix": "Studio Ghibli inspired artwork,",
        "suffix": "whimsical fantasy, soft watercolor textures, nostalgic atmosphere, hand-drawn animation style",
        "modifiers": ["Hayao Miyazaki style", "enchanted forest", "magical realism", "dreamy atmosphere"]
    },
    "oil_painting": {
        "prefix": "Oil painting,",
        "suffix": "traditional art, brush strokes visible, canvas texture",
        "modifiers": ["masterpiece", "museum quality", "classical technique"]
    },
    "watercolor": {
        "prefix": "Watercolor painting,",
        "suffix": "soft edges, flowing colors, paper texture, wet-on-wet technique",
        "modifiers": ["delicate brushwork", "transparent layers", "artistic"]
    },
    "digital_art": {
        "prefix": "Digital art,",
        "suffix": "digital painting, vibrant colors, clean lines, modern aesthetic",
        "modifiers": ["trending on DeviantArt", "digital illustration", "professional artwork"]
    },
    "3d_render": {
        "prefix": "3D render,",
        "suffix": "octane render, volumetric lighting, ray tracing",
        "modifiers": ["Unreal Engine 5", "photorealistic rendering", "4K textures"]
    },
    "3d_cartoon": {
        "prefix": "3D cartoon style,",
        "suffix": "Pixar-style animation, stylized 3D, colorful, animated movie quality",
        "modifiers": ["Disney animation style", "cartoon proportions", "vibrant colors"]
    },
    "pixar": {
        "prefix": "Pixar animation style,",
        "suffix": "3D animated movie quality, expressive characters, vibrant storytelling, cinematic lighting",
        "modifiers": ["Toy Story aesthetic", "emotional depth", "family-friendly", "photorealistic rendering"]
    },
    "disney": {
        "prefix": "Disney animation style,",
        "suffix": "classic Disney aesthetic, fairy tale atmosphere, musical animation quality",
        "modifiers": ["2D animation", "princess movie style", "magical kingdom", "hand-drawn charm"]
    },
    "dreamworks": {
        "prefix": "DreamWorks animation style,",
        "suffix": "modern 3D animation, dynamic action, comedic expressions, detailed environments",
        "modifiers": ["Shrek aesthetic", "How to Train Your Dragon style", "expressive faces", "cinematic quality"]
    },
    "concept_art": {
        "prefix": "Digital concept art,",
        "suffix": "professional illustration, detailed design, artstation quality",
        "modifiers": ["trending on artstation", "by professional concept artist", "production art"]
    },
    "pencil_sketch": {
        "prefix": "Pencil sketch,",
        "suffix": "detailed line art, graphite drawing, sketch style, hand-drawn",
        "modifiers": ["crosshatching", "shading", "artistic sketch"]
    },
    "ink_drawing": {
        "prefix": "Ink drawing,",
        "suffix": "pen and ink illustration, detailed linework, black and white art",
        "modifiers": ["hatching technique", "high contrast", "detailed illustration"]
    },
    "comic_book": {
        "prefix": "Comic book style,",
        "suffix": "bold outlines, vibrant colors, comic panel art, graphic novel style",
        "modifiers": ["Marvel/DC style", "speech bubbles", "action lines"]
    },
    "manga": {
        "prefix": "Manga style,",
        "suffix": "Japanese manga art, black and white, screen tones, expressive characters",
        "modifiers": ["shounen style", "detailed backgrounds", "speed lines"]
    },
    "makoto_shinkai": {
        "prefix": "Makoto Shinkai style artwork,",
        "suffix": "breathtaking landscapes, detailed clouds, lens flare, emotional atmosphere, anime movie quality",
        "modifiers": ["Your Name aesthetic", "photorealistic backgrounds", "romantic atmosphere", "detailed weather"]
    },
    "kyoto_animation": {
        "prefix": "Kyoto Animation style,",
        "suffix": "high quality anime, detailed character animation, soft lighting, emotional storytelling",
        "modifiers": ["K-ON style", "Violet Evergarden quality", "fluid animation", "moe aesthetic"]
    },
    "pixel_art": {
        "prefix": "Pixel art,",
        "suffix": "8-bit style, retro gaming aesthetic, pixelated, sprite art",
        "modifiers": ["16-bit", "retro game style", "limited color palette"]
    },
    "vector_art": {
        "prefix": "Vector illustration,",
        "suffix": "clean vector graphics, flat design, geometric shapes, scalable art",
        "modifiers": ["Adobe Illustrator style", "minimal design", "modern graphics"]
    },
    "impressionist": {
        "prefix": "Impressionist painting,",
        "suffix": "loose brushwork, light and color focus, Monet style, artistic interpretation",
        "modifiers": ["French impressionism", "outdoor lighting", "visible brushstrokes"]
    },
    "van_gogh": {
        "prefix": "Van Gogh style painting,",
        "suffix": "swirling brushstrokes, vibrant colors, post-impressionist technique, emotional intensity",
        "modifiers": ["Starry Night style", "thick impasto", "expressive strokes", "vivid yellows and blues"]
    },
    "monet": {
        "prefix": "Claude Monet style painting,",
        "suffix": "impressionist masterpiece, water lilies, soft light, atmospheric effects",
        "modifiers": ["garden scenes", "water reflections", "plein air painting", "natural light"]
    },
    "picasso": {
        "prefix": "Pablo Picasso style artwork,",
        "suffix": "cubist interpretation, geometric forms, multiple perspectives, abstract representation",
        "modifiers": ["Blue Period", "analytical cubism", "fragmented reality", "modernist approach"]
    },
    "dali": {
        "prefix": "Salvador Dali style surrealist art,",
        "suffix": "melting forms, dreamlike imagery, impossible physics, symbolic elements",
        "modifiers": ["melting clocks", "surreal landscapes", "paranoid-critical method", "optical illusions"]
    },
    "banksy": {
        "prefix": "Banksy style street art,",
        "suffix": "stencil graffiti, political satire, urban art, social commentary",
        "modifiers": ["wall art", "provocative message", "black and white stencil", "subversive humor"]
    },
    "expressionist": {
        "prefix": "Expressionist art,",
        "suffix": "emotional intensity, distorted forms, bold colors, subjective perspective",
        "modifiers": ["German expressionism", "emotional brushwork", "psychological depth"]
    },
    "surrealist": {
        "prefix": "Surrealist art,",
        "suffix": "dreamlike imagery, Salvador Dali style, impossible scenes, symbolic elements",
        "modifiers": ["subconscious imagery", "distorted reality", "artistic surrealism"]
    },
    "pop_art": {
        "prefix": "Pop art style,",
        "suffix": "Andy Warhol inspired, bold colors, Ben Day dots, commercial art aesthetic",
        "modifiers": ["Roy Lichtenstein style", "comic-inspired", "vibrant colors"]
    },
    "art_nouveau": {
        "prefix": "Art Nouveau style,",
        "suffix": "ornamental design, flowing organic lines, Alphonse Mucha inspired, decorative art",
        "modifiers": ["elegant curves", "natural motifs", "vintage poster style"]
    },
    "art_deco": {
        "prefix": "Art Deco style,",
        "suffix": "geometric patterns, luxury aesthetic, 1920s style, elegant symmetry",
        "modifiers": ["golden age design", "streamlined forms", "sophisticated elegance"]
    },
    "bauhaus": {
        "prefix": "Bauhaus style,",
        "suffix": "functional design, geometric simplicity, primary colors, modernist aesthetic",
        "modifiers": ["form follows function", "minimalist design", "industrial aesthetic"]
    },
    "steampunk": {
        "prefix": "Steampunk style,",
        "suffix": "Victorian era machinery, brass and copper, gears and steam, retro-futuristic",
        "modifiers": ["clockwork mechanisms", "industrial age", "neo-Victorian"]
    },
    "cyberpunk": {
        "prefix": "Cyberpunk style,",
        "suffix": "neon lights, futuristic city, high-tech low-life, dystopian aesthetic",
        "modifiers": ["Blade Runner aesthetic", "neon glow", "tech noir"]
    },
    "synthwave": {
        "prefix": "Synthwave aesthetic,",
        "suffix": "80s retro-futurism, neon grid, sunset colors, outrun style",
        "modifiers": ["retrowave", "neon aesthetic", "80s nostalgia"]
    },
    "vaporwave": {
        "prefix": "Vaporwave aesthetic,",
        "suffix": "80s/90s nostalgia, neon colors, glitch art, retro digital",
        "modifiers": ["aesthetic", "synthwave colors", "nostalgic vibes"]
    },
    "minimalist": {
        "prefix": "Minimalist design,",
        "suffix": "simple composition, clean lines, negative space, essential elements only",
        "modifiers": ["less is more", "modern minimal", "simplified forms"]
    },
    "maximalist": {
        "prefix": "Maximalist art,",
        "suffix": "excessive detail, ornate patterns, vibrant colors, more is more philosophy",
        "modifiers": ["baroque influence", "elaborate decoration", "visual abundance"]
    },
    "gothic": {
        "prefix": "Gothic art style,",
        "suffix": "dark atmosphere, medieval inspired, ornate details, dramatic shadows",
        "modifiers": ["dark fantasy", "cathedral architecture", "mysterious mood"]
    },
    "baroque": {
        "prefix": "Baroque style,",
        "suffix": "dramatic lighting, rich colors, dynamic movement, ornate details",
        "modifiers": ["chiaroscuro", "grand composition", "emotional intensity"]
    },
    "renaissance": {
        "prefix": "Renaissance painting style,",
        "suffix": "classical technique, Leonardo da Vinci inspired, realistic proportions, sfumato",
        "modifiers": ["Italian Renaissance", "classical art", "old master technique"]
    },
    "romanticism": {
        "prefix": "Romantic period art,",
        "suffix": "emotional expression, dramatic landscapes, sublime nature, passionate themes",
        "modifiers": ["Turner style", "emotional depth", "nature's grandeur"]
    },
    "abstract": {
        "prefix": "Abstract art,",
        "suffix": "non-representational, color and form focus, expressive composition",
        "modifiers": ["Kandinsky style", "geometric abstraction", "color field"]
    },
    "cubist": {
        "prefix": "Cubist art,",
        "suffix": "fragmented forms, multiple perspectives, Picasso style, geometric deconstruction",
        "modifiers": ["analytical cubism", "synthetic cubism", "avant-garde"]
    },
    "fauvism": {
        "prefix": "Fauvist painting,",
        "suffix": "wild colors, bold brushstrokes, Matisse style, emotional color use",
        "modifiers": ["les Fauves", "pure color", "expressive brushwork"]
    },
    "pointillism": {
        "prefix": "Pointillist painting,",
        "suffix": "dots of color, optical mixing, Seurat style, systematic technique",
        "modifiers": ["divisionism", "color theory", "precise dots"]
    },
    "low_poly": {
        "prefix": "Low poly 3D art,",
        "suffix": "geometric simplification, faceted surfaces, modern 3D aesthetic",
        "modifiers": ["polygonal art", "geometric 3D", "simplified geometry"]
    },
    "isometric": {
        "prefix": "Isometric illustration,",
        "suffix": "30-degree angles, technical drawing style, architectural precision",
        "modifiers": ["isometric projection", "technical illustration", "precise geometry"]
    },
    "flat_design": {
        "prefix": "Flat design illustration,",
        "suffix": "no shadows, simple shapes, bold colors, modern UI aesthetic",
        "modifiers": ["material design", "clean interface", "simplified icons"]
    },
    "line_art": {
        "prefix": "Line art illustration,",
        "suffix": "clean lines only, no shading, minimalist drawing, contour art",
        "modifiers": ["single line", "continuous line", "outline only"]
    },
    "chalk_art": {
        "prefix": "Chalk drawing,",
        "suffix": "pastel colors, textured surface, street art style, soft edges",
        "modifiers": ["sidewalk art", "pastel technique", "dusty texture"]
    },
    "charcoal": {
        "prefix": "Charcoal drawing,",
        "suffix": "deep blacks, smudged textures, dramatic contrast, artistic rendering",
        "modifiers": ["charcoal sketch", "tonal study", "expressive marks"]
    },
    "colored_pencil": {
        "prefix": "Colored pencil artwork,",
        "suffix": "layered colors, precise details, traditional medium, vibrant hues",
        "modifiers": ["prismacolor style", "realistic coloring", "detailed illustration"]
    },
    "pastel": {
        "prefix": "Pastel painting,",
        "suffix": "soft colors, blended tones, chalky texture, impressionistic style",
        "modifiers": ["soft pastels", "oil pastels", "gentle blending"]
    },
    "acrylic": {
        "prefix": "Acrylic painting,",
        "suffix": "bold colors, quick-drying paint, modern art technique, versatile medium",
        "modifiers": ["impasto technique", "fluid acrylics", "contemporary art"]
    },
    "gouache": {
        "prefix": "Gouache painting,",
        "suffix": "opaque watercolor, matte finish, illustration style, flat colors",
        "modifiers": ["designer gouache", "poster art", "commercial illustration"]
    },
    "graffiti": {
        "prefix": "Graffiti art,",
        "suffix": "street art style, spray paint aesthetic, urban art, bold tags",
        "modifiers": ["wildstyle", "bubble letters", "street culture"]
    },
    "stained_glass": {
        "prefix": "Stained glass art,",
        "suffix": "colored glass panels, lead lines, cathedral window style, luminous colors",
        "modifiers": ["Tiffany style", "religious art", "light transmission"]
    },
    "mosaic": {
        "prefix": "Mosaic art,",
        "suffix": "tile pieces, fragmented image, Byzantine style, decorative pattern",
        "modifiers": ["tessellation", "ceramic tiles", "ancient technique"]
    },
    "origami": {
        "prefix": "Origami style,",
        "suffix": "paper folding art, geometric forms, Japanese craft, angular shapes",
        "modifiers": ["paper art", "folded design", "minimalist sculpture"]
    },
    "papercut": {
        "prefix": "Papercut art,",
        "suffix": "layered paper, shadow box effect, intricate cutting, delicate design",
        "modifiers": ["kirigami", "paper sculpture", "silhouette art"]
    },
    "collage": {
        "prefix": "Collage artwork,",
        "suffix": "mixed media, layered elements, cut and paste aesthetic, artistic assembly",
        "modifiers": ["photomontage", "mixed materials", "dadaist style"]
    },
    "glitch_art": {
        "prefix": "Glitch art,",
        "suffix": "digital errors, corrupted data aesthetic, pixel sorting, distorted imagery",
        "modifiers": ["datamosh", "compression artifacts", "digital decay"]
    },
    "double_exposure": {
        "prefix": "Double exposure photography,",
        "suffix": "overlapping images, transparent layers, artistic blend, surreal combination",
        "modifiers": ["multiple exposure", "creative photography", "layered composition"]
    },
    "noir": {
        "prefix": "Film noir style,",
        "suffix": "high contrast black and white, dramatic shadows, 1940s detective aesthetic",
        "modifiers": ["chiaroscuro lighting", "venetian blinds", "mysterious atmosphere"]
    },
    "retro_futurism": {
        "prefix": "Retro-futuristic design,",
        "suffix": "vintage vision of future, atomic age aesthetic, 1950s sci-fi style",
        "modifiers": ["raygun gothic", "space age", "yesterday's tomorrow"]
    },
    "dieselpunk": {
        "prefix": "Dieselpunk aesthetic,",
        "suffix": "interwar period technology, diesel-powered machinery, alternate history",
        "modifiers": ["decopunk", "1930s-1940s style", "industrial warfare"]
    },
    "biopunk": {
        "prefix": "Biopunk style,",
        "suffix": "organic technology, genetic modification aesthetic, biological horror",
        "modifiers": ["organic machinery", "bio-horror", "genetic art"]
    },
    "solarpunk": {
        "prefix": "Solarpunk aesthetic,",
        "suffix": "eco-futurism, green technology, sustainable utopia, bright optimistic future",
        "modifiers": ["green architecture", "renewable energy", "hopeful future"]
    },
    "cottagecore": {
        "prefix": "Cottagecore aesthetic,",
        "suffix": "rural life romanticization, cozy countryside, pastoral beauty, vintage charm",
        "modifiers": ["countryside living", "homemade crafts", "nostalgic comfort"]
    },
    "dark_academia": {
        "prefix": "Dark academia aesthetic,",
        "suffix": "gothic university setting, classical literature, moody atmosphere, scholarly pursuit",
        "modifiers": ["ancient libraries", "candlelit study", "mysterious knowledge"]
    },
    "liminal_space": {
        "prefix": "Liminal space photography,",
        "suffix": "empty transitional spaces, eerie atmosphere, nostalgic unease, abandoned places",
        "modifiers": ["backrooms aesthetic", "empty malls", "uncanny feeling"]
    },
    "ukiyo_e": {
        "prefix": "Ukiyo-e Japanese woodblock print,",
        "suffix": "traditional Japanese art, flat colors, outlined forms, Hokusai style",
        "modifiers": ["floating world", "woodblock technique", "Edo period art"]
    },
    "sumi_e": {
        "prefix": "Sumi-e ink painting,",
        "suffix": "Japanese ink wash, minimalist brushwork, zen aesthetic, monochrome art",
        "modifiers": ["ink wash painting", "meditative art", "bamboo and mountains"]
    },
    "madhubani": {
        "prefix": "Madhubani painting,",
        "suffix": "Indian folk art, intricate patterns, vibrant colors, mythological themes",
        "modifiers": ["Mithila art", "Bihar folk painting", "traditional motifs"]
    },
    "aboriginal": {
        "prefix": "Aboriginal dot painting,",
        "suffix": "Australian indigenous art, dot technique, dreamtime stories, earth colors",
        "modifiers": ["indigenous Australian", "sacred patterns", "traditional symbols"]
    },
    "aztec": {
        "prefix": "Aztec art style,",
        "suffix": "Mesoamerican patterns, geometric designs, symbolic imagery, ancient aesthetic",
        "modifiers": ["pre-Columbian art", "Mexican heritage", "ritual symbolism"]
    },
    "celtic": {
        "prefix": "Celtic art style,",
        "suffix": "interlaced patterns, knotwork designs, illuminated manuscript style",
        "modifiers": ["Irish art", "Book of Kells style", "spiral patterns"]
    },
    "mandala": {
        "prefix": "Mandala art,",
        "suffix": "circular patterns, sacred geometry, meditative design, intricate symmetry",
        "modifiers": ["spiritual art", "radial symmetry", "zen patterns"]
    },
    "psychedelic": {
        "prefix": "Psychedelic art,",
        "suffix": "trippy visuals, swirling colors, optical illusions, 1960s aesthetic",
        "modifiers": ["acid art", "kaleidoscopic", "mind-bending visuals"]
    },
    "lowbrow": {
        "prefix": "Lowbrow pop surrealism,",
        "suffix": "underground art, cartoon influence, subversive themes, alternative culture",
        "modifiers": ["pop surrealism", "underground comix", "alternative art"]
    },
    "photomontage": {
        "prefix": "Photomontage composition,",
        "suffix": "combined photographs, surreal assembly, collage technique, manipulated reality",
        "modifiers": ["photo manipulation", "composite image", "digital collage"]
    }
}

def get_style_list():
    """Get list of all available style names"""
    return list(STYLE_PRESETS.keys()) + ["custom"]

def get_style_preset(style_name):
    """Get a specific style preset by name"""
    return STYLE_PRESETS.get(style_name, None)