### V0.00
- [x] 15min task to fetch highlights and create tweets

### URGENT:
- [x] !!! readwise fetch not happenin
- [x] fetch from last highlight timestamp to correct for gaps
- [x] two threads bein made for each discord-tweet flow
- [x] idea2thread bug
- [ ] health status message, error message
- [x] sonnet 3.5 (model selection)
- [x] prompt refinement
      - [x] meditation, philosophy, principles

### V0.01: personal posts
- [x] Discord text to tweet flow
  - [x] preserve original text in first tweet
  - [x] podcast transcript missing, original text = "20sec Snip"
  - [x] readwise highlight being transformed into thread instead of tweet
- [x] Discord text to thread flow
- [x] double thread being created, one through idea2tweet one through idea2thread - delete the thread

### Polishing:
- [ ] improve tweet prompt (same/better/best/different, problem/benefits/solution)
  - [ ] mine from Dan, Matt & Justin
  - [x] Prompt for tweet variations: Original text, Improved for tweet, Inspirational, Practical implementation, Risks of not implementing, Benefits of implementing
  - [ ] Prompt for threads: 
Give second option of listicle, depending on the input
- [ ] tweet remix flow - share X tweet URL to discord, fetch tweet text, send to tweet variations flow
- [ ] GPT 2 multi tweet draft

### Step Back
- [ ] plan project overview w. AI: describe goal and journey - ask how to approach with sound python software engineering practices
- [ ] figure out versioning
- [ ] high-level architecture re. back-end and front-end
  - [ ] I want to be considerate of building a progressive web app - many logins, markdown files per user, all calling on single back-end - or is there a better way? If this is the way, then the various text transformations may be better as endpoints...
  - [ ] input -> draft + notes
  - [ ] highlight notes -> transform notes / send to draft

### V0.02: store & org. published 'notes'
- [ ] fetch published posts (Typefully or X)
- [ ] store in weekly markdown notes

V.03 notes 2 newsletters
- [ ] transform weekly notes into a newsletter
- [ ] publish two/three draft newsletter options to Beehive

V.04: UI to replace Discord
- [ ] log in
- [ ] 'send' text bottom bar bubble
    - [ ] 'send' to tweet/thread/newsletter draft
- [ ] VNs

V.05: UI notes, files, folders
- [ ] markdown weekly notes main window
- [ ] left sidebar files/folders

V0.1: 
- [ ] highlights, notes -> weekly notes
- [ ] tweets/threads/newsletters usable for me personally
- [ ] ??? simple login and input to replace Discord

Future
- V1 UI:
    - login
    - OpenAI token (unless freemium? Llamma 408B)
    - Typefully token

BUGS:
- two threads of tweet options being created (instead of one)