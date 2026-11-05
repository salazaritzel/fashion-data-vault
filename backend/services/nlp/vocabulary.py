# Store vocabulary list on here so that it is easily maintainable as it grows (a machine learning model is the end goal but this will do for now)
materials = [
    "acetate", "acrylic", "alpaca", "angora",
    "bamboo", "bead", "bio-based", "boucle", "bouclé",
    "cactus leather", "canvas", "cashmere", "cashmere wool", "cellulosic fibers", "cellulosic fibres", "chambray", "chenille", "chiffon", "chitosan",
    "corduroy", "cork", "cotton", "crepe", "crêpe", "crochet", "crystal", "cupro",
    "damask", "denim",
    "ecovero", "elastane", "elastene", "elastin",
    "faux fur", "fishnet", "flannel", "flax", "fleece", "french terry", "fur",
    "gabardine", "gauze", "georgette", "gingham", "grosgrain",
    "hemp",
    "jacquard", "jelly", "jute",
    "lace", "lamé", "latex", "leather", "linen", "lurex", "lyocell",
    "merino", "merino wool", "mesh", "microfiber", "microfibre", "modal", "mohair", "muslin", "mycelium",
    "neoprene", "nubuck", "nylon",
    "organza", "oxford",
    "pearl", "pima cotton", "pinatex", "piñatex", "pique", "piqué", "pleather", "polyamide", "polyester", "polyvinyl chloride", "ponte", "poplin",
    "pvc",
    "raffia", "ramie", "rattan", "rayon", "recycled cotton", "recycled nylon", "recycled pet", "recycled polyester", "rhinestone", "ripstop",
    "rubber",
    "sateen", "satin", "seacell", "seersucker", "sequin", "shearling", "sherpa", "silk", "spandex", "spinnova", "straw", "suede",
    "taffeta", "tencel", "terry cloth", "toile", "toile de jouy", "tricot", "tulle", "tweed", "twill", "tyvek",
    "velour", "velvet", "velveteen", "vinyl", "vinylon", "viscose", "viscose rayon", "voile",
    "waffle knit", "wicker", "wool"
]

# TODO: Create aliases for brands (e.g. "YSL" for "Yves Saint Laurent", "LV" for "Louis Vuitton", etc.)
fashion_brands = [
    "16Arlington",
    "Acne Studios", "Adidas", "Alaïa", "Alexander McQueen", "Alexander Wang", "Amina Muaddi", "Armani", "Asics", "Azzedine Alaïa",
    "Badgley Mischka", "Balenciaga", "Balmain", "Bottega Veneta", "Brunello Cucinelli", "Bulgari", "Burberry", "Bvlgari",
    "Calvin Klein", "Carolina Herrera", "Cartier", "Casadei", "Celia Kritharioti", "Celine", "Chanel", "Chloé", "Chopard", "Christian Dior",
    "Christian Lacroix", "Christian Louboutin", "Christopher Esber", "Chrome Hearts", "Coach", "Comme des Garçons", "Coperni", "Courrèges",
    "DÔEN", "Dolce & Gabbana", "Dries Van Noten", "Dsquared2",
    "Elie Saab", "Emilio Pucci",
    "Fear of God", "Fendi", "Ferragamo",
    "Ganni", "Gianvito Rossi", "Giorgio Armani", "Giuseppe Zanotti", "Givenchy", "Gucci",
    "Helmut Lang", "Hermès", "Herve Leger", "Hugo Boss",
    "Isabel Marant", "Issey Miyake",
    "Jacquemus", "Jean Paul Gaultier", "Jil Sander", "Jimmy Choo", "John Galliano",
    "Kate Spade", "Khaite", "KNWLS",
    "Lacoste", "Lanvin", "Lemaire", "Loewe", "Loro Piana", "Louis Vuitton", "Lu'u Dan", "Luar",
    "Magliano", "Maison Margiela", "Manolo Blahnik", "Marc Jacobs", "Marni", "Max Mara", "Michael Kors", "Miss Sohee", "Miu Miu", "Moschino",
    "Mulberry",
    "New Balance", "Nike", "North Face",
    "Off-White", "Oscar de la Renta", "Ouma",
    "Paco Rabanne", "Pertegaz", "Prada", "Proenza Schouler", "Puma",
    "Ralph Lauren", "Rick Owens", "Robert Wun", "Roberto Cavalli", "Rodarte",
    "Sacai", "Saint Laurent", "Salomon", "Salvatore Ferragamo", "Schiaparelli", "Self-Portrait", "Simkhai", "Simone Rocha", "Soshiotsuki",
    "Stella McCartney",
    "The Attico", "The Row", "Thierry Mugler", "Thom Browne", "Tiffany", "Tom Ford", "Tory Burch", "Toteme",
    "Valentino", "Van Cleef & Arpels", "Vera Wang", "Versace", "Vetements", "Victoria Beckham", "Vivienne Westwood",
    "Y-3", "Yohji Yamamoto", "YSL", "Yves Saint Laurent",
    "Zac Posen", "Zara", "Zimmermann", "Zuhair Murad"
]

fashion_nouns = [
    "accessory",
    "backpack", "bag", "baguette", "bandana", "bangle", "beanie", "belt", "beret", "bikini", "blazer", "blouse", "bodysuit", "boot", "bootie", "bow",
    "bracelet", "bralette", "brooch",
    "camisole", "cape", "cardigan", "choker", "clog", "clutch", "coat", "corset", "corsetry",
    "dress",
    "earring", "eveningwear",
    "flat",
    "glove", "gown",
    "handbag", "hat", "headband", "heel", "hoodie",
    "jacket", "jean", "jewellery", "jewelry", "jumper", "jumpsuit",
    "kimono", "knitwear",
    "legging", "lingerie", "loafer",
    "mule",
    "necklace",
    "outerwear", "overcoat",
    "pant", "parka", "peacoat", "pendant", "poncho", "puffer", "pump", "purse",
    "raincoat", "robe", "romper",
    "sandal", "satchel", "scarf", "shawl", "shirt", "shoe", "skirt", "skort", "slide", "slingback", "slipper", "sneaker", "stiletto", "suit",
    "sunglass", "sweater", "sweatshirt", "swimsuit",
    "tee", "t-shirt", "tank", "top", "tote", "tracksuit", "trainer", "trench", "trouser", "tunic", "turtleneck", "tuxedo",
    "undergarment",
    "vest",
    "wallet", "watch", "wedge"
]

fashion_adjectives = [
    "argyle", "asymmetrical", "a-line",
    "babydoll", "backless", "baggy", "ballet", "balloon", "barn", "barrel", "basic", "bespoke", "birkin", "bodycon", "bomber", "bootcut", "boxy",
    "boyfriend", "button-down", "button-up",
    "cable", "camo", "capri", "cargo", "cheeky", "chunky", "collar", "colorful", "column", "corset", "cowboy", "cowl", "cozy", "crew", "crew-neck", "crop", "crossbody",
    "cutout",
    "distress", "distressed", "double-breasted", "drape", "duster",
    "embellish", "embossed", "embroider",
    "faded", "faux", "fit", "fitted", "flare", "floor-length", "floral", "flowy", "fray", "frayed", "fringe", "full",
    "gladiator", "glossy", "graphic",
    "halter", "handcrafted", "high-rise", "herringbone", "holographic", "houndstooth", "hug",
    "iridescent",
    "jeweled",
    "kitten", "knee-length", "knit",
    "lace-up", "layered", "leopard", "lightweight", "longline", "loose", "low", "low-rise",
    "matte", "maxi", "mermaid", "metallic", "midi", "mid-rise", "military", "mini", "miniskirt", "monochrome",
    "naked", "nap", "neon",
    "off-the-shoulder", "ombre", "over-the-knee", "oversize",
    "pad", "padded", "paisley", "pastel", "patchwork", "patent", "pencil", "penny", "perforated", "pillbox", "pinstripe", "plaid", "pleated",
    "plunge", "polish", "polka", "polo", "prairie", "print",
    "quilt", "quilted",
    "relax", "retro", "rib", "ribbed", "ruche", "ruched", "ruffle",
    "scoop", "sculptural", "semi-sheer", "sheer", "shimmer", "shoulder", "skinny", "skinny-leg", "skirt", "sleek", "sleeveless", "slim", "slip", "slouchy", "smock",
    "smocked", "snakeskin", "straight", "straight-leg", "strapless", "strappy", "striped", "structure", "stud", "studded", "sweatpant",
    "tailor", "tall", "tank", "tapered", "tartan", "thigh-high", "tennis", "tiered", "tote", "track", "trench", "trim",
    "vintage", "voluminous", "v-neck",
    "weave", "wedge", "wide-leg", "wrap",
    "zebra"
]

colors = [
    "alabaster", "alice blue", "amaranth", "amber", "apple green", "apricot", "aqua", "aquamarine", "army green", "artichoke", "ash gray",
    "auburn", "avocado", "azure",
    "baby blue", "baby pink", "barn red", "battleship gray", "beige", "bisque", "black", "black olive", "blood red", "blue", "blush pink",
    "bone", "bottle green", "brass", "brick red", "bright blue", "bright red", "brink pink", "brown", "bubblegum", "buff", "burgundy",
    "burnt umber", "butter yellow", "butterscotch",
    "cadmium red", "cadmium yellow", "camel", "canary yellow", "candy apple red", "carmine", "carnation pink", "carrot", "celadon",
    "celery", "celeste", "celtic blue", "cerise", "cerulean", "champagne", "charcoal", "charleston green", "chartreuse", "cherry",
    "cherry blossom", "chestnut", "chocolate", "cinnabar", "cinnamon", "citron", "claret", "cobalt", "cocoa", "copper", "coquelicot",
    "coral", "cordovan", "cornflower blue", "cotton candy", "cream", "crimson", "cyan",
    "dark blue", "dark orange", "dark red", "dill", "duck blue",
    "ebony", "ecru", "eggplant", "eggshell", "electric blue", "emerald", "espresso", "eucalyptus",
    "fandango", "fern green", "fire engine red", "fluorescent blue", "forest green", "fuchsia",
    "gainsboro", "garnet", "ghost white", "gold", "goldenrod", "grape", "gray", "green", "green tea", "grey", "gunmetal",
    "heliotrope", "honeydew", "hot pink",
    "indigo", "international orange", "ivory",
    "jade", "jasper", "jungle green",
    "khaki", "kobicha",
    "lake blue", "lava red", "lavender", "lawn green", "lemon", "light green", "lilac", "lime",
    "madder", "magenta", "mahogany", "malachite", "mantis", "marigold", "maroon", "mauve", "melon", "midnight blue", "mineral red", "mint",
    "mint green", "mocha", "moss green", "mustard", "myrtle green",
    "navy", "neon red", "nickel", "nude",
    "oatmeal", "ochre", "olive", "onyx", "orange", "orchid", "oxblood",
    "paris green", "peach", "pear", "pearl white", "periwinkle", "persimmon", "phthalo blue", "pine green", "pink", "platinum", "plum", "polynesian blue",
    "powder blue", "pumpkin", "purple",
    "raspberry", "rebecca purple", "red", "reddish brown", "robin egg blue", "rose gold", "rose vale", "rosewood", "royal blue",
    "ruby", "ruddy blue", "russet", "rust",
    "safety orange", "safety yellow", "saffron", "sage", "salmon", "sandy brown", "sap green", "sapphire", "scarlet", "sea green",
    "seashell", "shocking pink", "silver", "sky blue", "slate gray", "spanish blue", "stone gray",
    "tan", "tangerine", "taupe", "teal", "terracotta", "tomato", "turquoise", "turtle green", "tyrian purple",
    "ultramarine", "umber",
    "vanilla", "verdigris", "vermilion", "violet", "viridian",
    "walnut", "wheat", "white", "wisteria", "wood brown",
    "yellow"
]

aesthetics = [
    "minimalist", "maximalist", "boho", "preppy", "grunge", "punk",
    "goth", "sporty", "edgy", "coquette", 
    "clean girl", "showgirl", "boho-grunge", "gorpcore", "quiet luxury", 
    "old money", "balletcore", "cottagecore", "y2k", "mob wife"
]

prints = [
       "animal print", "leopard print", "leopard", "cheetah", "zebra", "snakeskin",
       "snake print", "croc", "cow print", "tiger stripe", "plaid", "gingham",
       "houndstooth", "polka dot", "stripe", "paisley", "floral", "tartan",
       "argyle", "camo", "check",
]

fashion_collections = [
    "haute couture", "couture", "ready-to-wear", "womenswear", "menswear" 
]

# Different variants of the phrase in the format {Canonical: Variants} (TODO: Brands)
variants = {
    "high-rise": ["high rise", "high-waist", "high waist", "high waisted", "high-waisted"],
    "low-rise": ["low rise", "low-waist", "low waist", "low waisted", "low-waisted"],
    "mid-rise": ["mid rise", "mid-waist", "mid waist", "mid waisted", "mid-waisted"],
    "wide-leg": ["wide leg", "wide legged", "wide-legged"],
    "straight-leg": ["straight leg", "straight legged", "straight-legged"],
    "skinny-leg": ["skinny leg"],
    "floor-length": ["floor length"],
    "knee-length": ["knee length"],
    "over-the-knee": ["over the knee"],
    "thigh-high": ["thigh high"],
    "v-neck": ["v neck"],
    "crew-neck": ["crew neck"],
    "off-the-shoulder": ["off the shoulder"],
    "double-breasted": ["double breasted"],
    "button-down": ["button down"],
    "button-up": ["button up"],
    "lace-up": ["lace up"],
    "semi-sheer": ["semi sheer"],
    "faux fur": ["fake fur", "faux-fur"],
    "t-shirt": ["t-shirts"],
}

season_variants = {
    "spring": ["spring", "ss", "s-s", "s/s", "spring/summer", "spring summer", "spring-summer"],
    "fall": ["fw", "aw", "f/w", "a/w", "fall/winter", "autumn/winter", "autumn", "fall", "fall-winter", "autumn-winter", "fall winter", "autumn winter"],
    "resort": ["resort", "cruise"],
    "pre-fall": ["prefall", "pre fall", "pre/fall", "pre-fall"],
    "winter": ["winter"],
    "summer": ["summer"]
}

excluded_phrases = {
    "devil wears prada",
    "red carpet",
    "black tie",
    "black friday"
}