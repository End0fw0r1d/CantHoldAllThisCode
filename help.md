Anywhere that a command outputs text, it can be fed into [text to render]
Anywhere a command outputs an image, it can (almost always) be fed into where an [emoji] sits
Nested command structure is as
  - !command (command (command image/text args) args) args

BUT WITHOUT THE (parentheses)

------------

RENDERING COMMANDS:

- **intensify** [text to render] [red 0-255] [green 0-255] [blue 0-255] [intensity of vibration 0-infinity] : outputs the input text as a vibrating gif with colors RGB, centered and wrapped
- **speed** [text to render] [red 0-255] [green 0-255] [blue 0-255] [delay between words in X times .1 of second, minimum input of 2] : outputs the input text as RGB gif, 1 word per frame, cofigurable delay between frames
- **mocking** [text to render] : outputs a spongebob mocking meme with input text
- **shoot** [emoji] : outputs a monkashoot shooting the emoji out of a gun
- **space** [emoji] : outputs input emoji floating through space
- **italics** [emoji] : outputs input emoji as a slanted version of itself
- **jpeg** [emoji] : outputs a simply deep-fried image
- **jpeg2** [emoji] [iterations 0-infinity] : outputs a deep-fried image, with additional applications of deep-fry specified by arg
- **jpeg3** [emoji] [iterations 0-infinity] : outputs a jpegified image, with additional applications of jpeg specified by arg
- **weee** [emoji] : outputs a tiled, rotating, looping image
- **shake** [emoji] : outputs a mildly shaking image
- **moreshake** [emoji] : outputs a moderately shaking image
- **hold** [emoji] : outputs a 'cant hold all these limes' meme, but with emoji instead of limes
- **hold2** [emoji] : outputs as above, but gifs are given randomized frame-start offsets
- **overlay** [emoji] [string "hazmat" "hazmatf" "mask" "maskf"] : outputs an emoji, overlayed with a bttv hazmat suit or mask, the F at the end gives a flipped version
- **overlay2** [emoji] [string] [x offset] [y offset] [rotation in degrees] [scale 1 default, minimum of greater than 0] : same as above, but more configurable... and spammy
- **4head** [emoji] [intensity any integer, 0 is no change] : basically renders a sine-wave based distance-from-center on the image, positive values less than 30 balloon the image
- **wormhole** [emoji] : creates a gif where a 4head operation, each slightly different, is applied in succession with each frame
- **peek** [emoji] : makes the input emoji animate and peek over the bottom edge
- **peek2** [emoji] [height float 0-1] : simplified 1-step peek, peek height is 0-1 of the image height, 0.5 being halfway
- **rotate** [emoji] [degrees] : rotates the input emoji clockwise by input degrees
- **flip** [emoji] : flips the emoji left/right
- **hyper** [emoji] [look duration 1-infinity, but with caveats] : makes the emoji flip side-to-side with a delay between flips of 0.1X + 0.1, not necessarily evenly split into duration
- **info** [emoji] : outputs some text-based information about the input image, mostly for debug
- **8ball** : returns a text string of randomized 8ball responses, for feeding into text-input rendering commands


------------



MISC:

- **boys** : returns playercount of minecraft server
- **conch** : returns randomized 8ball responses, directly into chat
- **why** : for the glory of satan, of course!
- **navyseal** : outputs a pre-rendered speed text of the navyseal copypasta
- **I** [guess] : outputs a gif of the "I guess?" meme
- **God** : outputs meme webm
