# Those who bought the M5 Studio Max or Ultra, how is it working for you in real life work flow?  I'm mostly interested in agentic coding.

- 来源:r/MacStudio · 作者 According_Wave685 · 2026-10-25T19:18:40 · 分数 43 · 评论 96(本页抓到 25)
- 原链接:https://www.reddit.com/r/MacStudio/comments/1xfb4uk/those_who_bought_the_m5_studio_max_or_ultra_how/

> ⚠️ 以下引用块为逐字原件,未改写。

## 正文

> I was running dual GB10's, which was great, but with recent price bumps I decided to cash those in and add a second strix halo on which I can get almost the same speed.
>
>  Now I get 6 lanes of 262k across two strix halos load balanced with litellm. With Q38FN I get about 1800 prefill and 80 gen for coding for a single request. I quite often have multiple sub agents going so that speed will drop somewhat.
>
>  I am a software engineer working for 40 years (not a recent vibe coder who calls themselves a software engineer). I find AI convenient for off loading tasks to do my job. My employer requires me to keep everything local if I am going to use AI.
>
>  So I guess what I am asking, how is the new Mac working for you in this type of workflow? And tell me which model mac you have. What LLM you run to do your job, and at what quant with what engine.
>
>  Thanks!

## 评论

- **10fak1nd** · 7 分 · 2026-10-25T22:57:43 · <https://www.reddit.com/r/MacStudio/comments/1xfb4uk/comment/19rnjvdc40rcw/>

  > Enjoying it so far! Running GLM flash. Smooth, a lot faster than the M3U (512g)
  > Will look to order the 512g version, when it becomes available.

  - **According_Wave685** [OP] · 2 分 · 2026-10-25T23:14:42 · <https://www.reddit.com/r/MacStudio/comments/1xfb4uk/comment/19rnkmn8ud66a/>

    > Have you benchmarked  that model on that machine both single and concurrent requests at different context sizes?

- **BeneficialFall7415** · 7 分 · 2026-10-25T22:35:38 · <https://www.reddit.com/r/MacStudio/comments/1xfb4uk/comment/19rnivwlmva0z/>

  > i have 4x dgx spark and wanted to get my hands on 512gb m5u once its released; but some of the comments over here really worry me

  - **According_Wave685** [OP] · 2 分 · 2026-10-25T22:49:00 · <https://www.reddit.com/r/MacStudio/comments/1xfb4uk/comment/19rnjhctlkebp/>

    > Yeah I'm starting to reach the same conclusion.

  - **Healthy-Contact-4570** · 5 分 · 2026-10-26T00:27:54 · <https://www.reddit.com/r/MacStudio/comments/1xfb4uk/comment/19rnnw5tto4n8/>

    > 4x DGX sparks will crush m5u in inference. The memory bandwidth numbers might look appealing at first glance but they are not the whole story. Lack of hardware-level instructions for certain data types, poor software support, etc.
    >
    >  I have 4 sparks, I run deepseek V4.1 flash 1017, full fat GLM-5.3, etc

- **GCoderDCoder** · 5 分 · 2026-10-25T20:50:33 · <https://www.reddit.com/r/MacStudio/comments/1xfb4uk/comment/19rne7609stq8/>

  > How are you getting the same speed on strix halo as dual sparks? did you somehow connect the two halos via pcie slots in tp? before prices increased i sold my macs and strix halo for 4 sparks. my dual spark speeds with nvfp4 and better performance on mtp catches my sparks up to higher bandwidth devices like mac studios while needing less ram with low bit high fidelity versions like nvfp4 and exl3 the latter of which still seems to prefer cuda and has fewer mac options typically than cuda.
  >
  >  Edit: i got a m5max macbook as my mobile workstation and smaller 64gb m5max mac studio as a desktop hub for my agent services and tools. i prefer cuda for inference but depending on the use case and current pricing mac can be a decent value. but qwen 3.8 flash next for example i need at least q6 on mac for satisfactory performance and it's still not as good as nvfp4 imo. nvfp4 passes deep swe and terminal bench easier than q6 on mac. it's more than kl divergence with matching tokens vs identical tokens...

  - **According_Wave685** [OP] · 3 分 · 2026-10-25T21:34:51 · <https://www.reddit.com/r/MacStudio/comments/1xfb4uk/comment/19rng6axwxldt/>

    > It doesn't beat my dual gb10's (they were the MSI variant) at all, but it's an acceptable replacement. I am running halogen on both halos load balanced with sticky sessions so i don't lose out on cache hits. While it's not better than sparks, it's close enough. I'm just wondering if a Mac would be a better option or not.

  - **Rice-Fragrant** · 1 分 · 2026-10-26T10:49:31 · <https://www.reddit.com/r/MacStudio/comments/1xfb4uk/comment/19rofmao71z0g/>

    > I was wandering the same exact thing... Agents on a spark running like 5x faster for agentic looping than on AMD strix or Gorgon Halo.

    - **According_Wave685** [OP] · 1 分 · 2026-10-27T22:24:53 · <https://www.reddit.com/r/MacStudio/comments/1xfb4uk/comment/19rr2v1ijux6r/>

      > No it's not 5x faster at all. Based on my experience with both it's maybe 20% faster. Yes prefill get's 2-4k prefill,, but my halos get 1-2kk. So in real workflow I'mm not seeing a lot of difference. Halogen rocks.

  - **xyloid_x** · 3 分 · 2026-10-25T21:10:00 · <https://www.reddit.com/r/MacStudio/comments/1xfb4uk/comment/19rnf2emx1itc/>

    > Appreciate the info about quality, I rarely saw people talking about it, but I am super curious about it.

    - **GCoderDCoder** · 5 分 · 2026-10-25T21:20:36 · <https://www.reddit.com/r/MacStudio/comments/1xfb4uk/comment/19rnfjfkhl8ck/>

      > I initially wasted money on hardware that fell short of my expectations so I try to share my experiences before others with less disposable income burn their money too. with so much of this stuff the answer is "it depends" on needs and expectations. I had older cuda that I didn't love as much. I absolutely love what my sparks are letting me run.
      >
      >  I think Mac is better for multimodal but when people plan inference only for macs it's important to know macs have more inference quirks. mtp on certain models can actually be slower for example. or certain runtimes can only do mtp or concurrency but not both. i haven't had that experience with cuda to date yet like I repeatedly have had with Macs.

- **SnowOverflow** · 6 分 · 2026-10-27T03:44:38 · <https://www.reddit.com/r/MacStudio/comments/1xfb4uk/comment/19rpow9estqbk/>

  > I have a M5 Max MacBook Pro with 128GB RAM, initially I hoped that I could run local coding models but the reality is frontier models are still much faster and in higher quality so I stopped the hassle there

  - **BourbonicFisky** · 2 分 · 2026-10-28T02:51:27 · <https://www.reddit.com/r/MacStudio/comments/1xfb4uk/comment/19rrer2kokeir/>

    > Senior dev with 15+ years of experience. This has been my observation. The only person I knew who bought two M3 Ultras with 512 GB of RAM literally was defense contractor and could not use online models. It was slow as all get out and not nearly as good. Any port in a storm. The proof of concept meant he was able to get his work to purchase larger solutions for onsite as right now, business is booming thanks to a truly stupid war.
    >
    >  Anyone who's trying to seriously cut out the expensive AI services are going to be sorely disappointed as the non-quantized 2.8 billion param Kimi K3 is waaaay out of reach for mere mortals as its 1.5 TB.
    >
    >  I just went with a M5 Max + 64 GB of RAM and figure I'll continue to pay $100 + $100 for Claude and ChatGPT as even stepping to the ultra with 256 GB of RAM is a comical $11,299.00. That's 4.5 years of subscription services just to run moderately useful LLMs. The math ain't mathing.

- **migs647** · 12 分 · 2026-10-25T19:44:31 · <https://www.reddit.com/r/MacStudio/comments/1xfb4uk/comment/19rnb95imisg3/>

  > I can't speak to the Mac Studio, but I can speak from two other perspectives. M4 Max 128gb and RTX Pro 6000 Blackwell (in single and dual card setup).
  >
  >  The M4 Max, I've been able to do some smaller models like Qwen 2.5 7B coder for quick code completion with Zig. I've been a Mac dev since 2004 and a mobile (iOS, Android) engineer since 2009. When I run some bigger models for coding, it just hasn't been worth it on the M4 Max. It drags down performance to where I just use my company tool which utilizes Opencode under the hood to talk to my vLLM Blackwell setup that runs Qwen 3.8 27b NVFP4.
  >
  >  I have a M5 80gpu / 96gb on order, but won't be here for a few more weeks. With that said M4 Max has handled fine-tuning well, but I don't do anything else during that time besides browse the web.

  - **oss-jiiim** · 4 分 · 2026-10-25T20:43:15 · <https://www.reddit.com/r/MacStudio/comments/1xfb4uk/comment/19rndvfw8idts/>

    > I also have an M4 Max 128GB Mac Studio and I think the current best coding option is Qwen 3.8 Flash Next at Q4 with BF16 n-grams. I run that with Dwarf Star via DS Menu Bar and I get ~650 t/s prefill and ~55 t/s generation on my M4. An M5 will get at least double if not more for prefill, and better generation, too.
    >
    >  Disclosure: I made DS Menu Bar ;)

- **ln28909** · 3 分 · 2026-10-25T23:43:25 · <https://www.reddit.com/r/MacStudio/comments/1xfb4uk/comment/19rnlwqyy24qp/>

  > I have M5U 96gb running Swift QFN IQ3_S on splash
  > Prefill: 3000 tok/s
  > Decode: 150tok/s (single), 73 tok/s (3 active requests, aggregate 218tok/s), context length above 100k

- **uxor-moecha-amans** · 2 分 · 2026-10-26T03:41:55 · <https://www.reddit.com/r/MacStudio/comments/1xfb4uk/comment/19rnwjpkw9wu8/>

  > Waiting for the 512GB M5 Ultra.

- **Simple_Telephone_867** · 2 分 · 2026-10-26T04:32:57 · <https://www.reddit.com/r/MacStudio/comments/1xfb4uk/comment/19rnytnnng1he/>

  > Got the M5 Max 128GB and it has been amazing.
  >
  >  If you’re developing iOS, working with multi agent workflows, concurrency, all have phenomenal speeds.
  >
  >  I was hesitating between the M5U and the M5M and I’m glad I got the Max.

- **Lurkerade82** · 3 分 · 2026-10-26T02:00:56 · <https://www.reddit.com/r/MacStudio/comments/1xfb4uk/comment/19rns1jm1fnnn/>

  > I’m an Apple developer with a 128g M5 Max mbp.
  > I created a team by allowing Claude to have computer control and use Chatgpt, Gemini & Kimi K as subagents, taking advantage of their unique school sets respectively.
  > I’ve created five apps recently, all on the one system, and it works flawlessly

- **jiqiren** · 2 分 · 2026-10-25T21:05:18 · <https://www.reddit.com/r/MacStudio/comments/1xfb4uk/comment/19rneuui3izcw/>

  > Unfortunately my ship date isn’t until the end of November for my M5Ultra 256GB. Right now I have Mac mini M4 Pro 64GB and it can do qwen3.8 very slowly with about 96-128k context. Quality is pretty good so I already feel confident with Mac Studio incoming.
  >
  >  I want local because I’m using financial documents and bank data so I don’t want a 3rd party to have access.

- **Ok_Warning2146** · 1 分 · 2026-10-26T04:45:56 · <https://www.reddit.com/r/MacStudio/comments/1xfb4uk/comment/19rnzei09wc5f/>

  > I think M5U 512gb can give you a good start for local AI. Then when Rubin Sparks come out in 2028, u can switch to it for faster performance and better clustering.

- **Reasonable_Bug_6501** · 1 分 · 2026-10-26T13:44:26 · <https://www.reddit.com/r/MacStudio/comments/1xfb4uk/comment/19ronf5sn5e9v/>

  > I’m new to the local A.I. scene and know nothing of coding. Been using my 395+ gaming handheld before this for automated script work.
  > So, I’ve been having an absolute blast with my ultra 256. It’s been so fun learning how to use it to create local agents to assist me in my work. I’m loving how I’ve been able to automate parts of my workflow that my industry mostly hasn’t even begun to catch on to. Every second saved is a second that I’ve bought back for the other things in life that actually matters

- **Kritblade** · 1 分 · 2026-10-26T13:58:47 · <https://www.reddit.com/r/MacStudio/comments/1xfb4uk/comment/19roo2707p8jp/>

  > Qwen 3.8 next flash splash 176B A6B 4bit on M5U 80core 96GB. The prefill with 80c is damn quick, I personally think it's well worth the money.

- **RyanElectrified** · 1 分 · 2026-10-27T15:05:11 · <https://www.reddit.com/r/MacStudio/comments/1xfb4uk/comment/19rqj919igq69/>

  > Right, you need to become a vibe coder, engineer. I am not saying you have this issue, but you know what your discussion of people "pretending" kind of hints to me you do hve the issue, anyway I've seen it, the issue is they think their experience has to be important, so they human bottleneck the process.
  >
  >  AI pair programming means you can use your experience as a manager; you cannot use your experience for low level tasks any more. If you do, you are not unlocking AI.
  >
  >  I have 30 years' experience and can recall the pre-AI days, but I do not human bottleneck, just to share the scope: I used 4.5 billion tokens last month. That's, over 1700 tok/s running 24/7. Compare that to the 250 million tokens your mac could produce if it ran 24/7 producing nothing but tokens at 100 tok/s - which is all these folks are hoping for...You just won't get to the promised land with your Mac.
  >
  >  The people who recommend this, are human bottlenecking. They are doing something they enjoy as a hobby, which is fine, but they are way behind the curve.
  >
  >  The numbers don't work for local. What you need to investigate, is private links and agreements that prevent Microsoft (or whoever you trust, Amazon, Snowflake) from training on data, so you can solve your privacy concerns while being able to scale up well beyond anything the Mac could produce.
  >
  >  Now if your employer is just not going to move into the modern world...ok but personally I would not want to be working for that employer as things shift....the shift is occurring now, and will be massive over the next 2 years.

- **T-Rex_MD** · 1 分 · 2026-10-25T19:54:17 · <https://www.reddit.com/r/MacStudio/comments/1xfb4uk/comment/19rnbotywriit/>

  > Supper disappointed, clustering doesn't work as well as I had hoped.
  >
  >  Coming from an M3 512GB, now I know 512 is the lowest one can go.
  >
  >  Going to buy 2x M5U 512 tomorrow and return these.
