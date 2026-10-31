# Mac Studio M5 Ultra Buyers - Buyers Remorse?

- 来源:r/MacStudio · 作者 redmormon · 2026-10-17T04:36:48 · 分数 79 · 评论 110(本页抓到 25)
- 原链接:https://www.reddit.com/r/MacStudio/comments/1x815vj/mac_studio_m5_ultra_buyers_buyers_remorse/

> ⚠️ 以下引用块为逐字原件,未改写。

## 正文

> Hello Mac Studio Ultra owners :) There are still very few reviews about the Mac Studio M5 Ultra on the internet. For people like me who are thinking about buying M5 Ultra for local AI, video and image rendering and coding, we would love to hear your experiences.
>
>  I'd love to hear from real buyers:
>
>  Studio Model (Chip, GPU and RAM):
>
>  Using it for:
>
>  Favorite local AI models:
>
>  User experience so far:
>
>  Remorse / Regret: Yes, No
>
>  Further advice on anything:

## 评论

- **redmormon** [OP] · 17 分 · 2026-10-17T09:24:36 · <https://www.reddit.com/r/MacStudio/comments/1x815vj/comment/ph9vqjz/>

  > I found in a benchmark that the two Mac Studio M5 Ultra 256GB variations with 64c and 80c GPU are performing virtually identical. It seems the more GPU cores really only make a difference for video rendering, not AI or LLM.
  >
  >  https://omlx.ai/benchmarks/performance?chip=M5&context=131072&cursor=WyJwZXJmb3JtYW5jZTpjaGlwPU01JmNvbnRleHQ9MTMxMDcyJmRldmljZT0lNUIlMjJNNSUyMiUyQyUyMlVsdHJhJTIyJTVEJmhpZGVfc3BlY3ByZWZpbGw9MSZtZW1vcnlfbWluPTI1NiZzb3J0PXRnX3RwcyIsMTQwLDUzNzA3NCwyLDQsMzBd&device=%5B%22M5%22%2C%22Ultra%22%5D&hide_specprefill=1&memory_min=256&sort=tg_tps
  >
  >  32
  >
  >  M5 Ultra (80c)
  >
  >  256 GB
  >
  >  GLM-5.3-Flash-oQ4e-mtp 
  >
  >  4bit
  >
  >  128k
  >
  >  2,243
  >
  >  138.7
  >
  >  ✓
  >
  >  10-10
  >
  >  33
  >
  >  M5 Ultra (64c)
  >
  >  256 GB
  >
  >  GLM-5.3-Flash-oQ4e-mtp 
  >
  >  4bit
  >
  >  128k
  >
  >  1,848
  >
  >  138.5
  >
  >  ✓
  >
  >  10-14

  - **Relaxxxxing** · 6 分 · 2026-10-17T16:03:06 · <https://www.reddit.com/r/MacStudio/comments/1x815vj/comment/phbqr0m/>

    > The extra GPU cores improve prefill

  - **marnovo** · 6 分 · 2026-10-17T10:20:12 · <https://www.reddit.com/r/MacStudio/comments/1x815vj/comment/pha2bcn/>

    > Thanks, handy chart. In generation indeed very close as bandwidth bound, but you see the 25% extra cores delivering around 20% faster prefill which is arguably the weaker side of Apple silicon for AI. Now if that's worth the reasonable price difference it's up to one's use cases.

- **TaareVekhdeRahe** · 42 分 · 2026-10-17T04:52:23 · <https://www.reddit.com/r/MacStudio/comments/1x815vj/comment/ph8yplg/>

  > M5 ultra - 96gb - 1tb storage.
  >
  >  Satisfied with local model performance and computing overall. No regrets. Geocoded 150,000 addresses in novainim at like 200 addresses a second, saving me $700 in google geocoder calls 😎

  - **redmormon** [OP] · 5 分 · 2026-10-17T08:46:43 · <https://www.reddit.com/r/MacStudio/comments/1x815vj/comment/ph9rd28/>

    > "novainim" do you mean neovim?

- **tempfoot** · 13 分 · 2026-10-17T06:37:33 · <https://www.reddit.com/r/MacStudio/comments/1x815vj/comment/ph9bznp/>

  > Still waiting for my M5U/80/256....which I ordered on the day of the announcement...albeit late in the day.
  >
  >  I was, however, very lucky to get an M5 Max/40/128 MacBook pro, on sale, at Microcenter 2 weeks before the price increase.
  >
  >  I'm a non-coder, but I can't have my data leaving my network. (Legal and highly confidential finance work). As a result, some kv caching strategies are not as helpful, even for agentic turns as pure coding scenarios.
  >
  >  That said, on the 128gb M5 Max, Qwen Flash Next on MTPLX has been the "eureka" situation for me. The first performant local model that immediately struck me as reliably and consistently 'smart' enough to work on complex, interrelated sophisticated document and financial analysis and writing projects.
  >
  >  Today's work session showing peak generation at 120tok/s (seems to average roughly 80 across context usage) and 1645 t/s average prefill, 2333 peak.
  >
  >  My studio ship date is Nov 11-22. I may cancel and order a 512gb depending on pricing. Ironically the very useful output from a portable M5 Max 128 is making me wonder how much incremental benefit I will get from larger models.

  - **redmormon** [OP] · 4 分 · 2026-10-17T08:48:47 · <https://www.reddit.com/r/MacStudio/comments/1x815vj/comment/ph9rlny/>

    > Very interesting, what harness and engine do you use?

    - **tempfoot** · 3 分 · 2026-10-17T15:32:04 · <https://www.reddit.com/r/MacStudio/comments/1x815vj/comment/phbjzu5/>

      > MTPLX engine + Openwebui. Some small projects through Hermes.

- **fasteddie7** · 4 分 · 2026-10-17T05:22:03 · <https://www.reddit.com/r/MacStudio/comments/1x815vj/comment/ph92l29/>

  > I got mine a few days ago and in some things it’s similar to the m3 ultra, and others it blows it away. I’ll have a full video comparing the 4 studios I have in the next few days, hopefully it’ll help.

  - **redmormon** [OP] · 3 分 · 2026-10-17T08:51:23 · <https://www.reddit.com/r/MacStudio/comments/1x815vj/comment/ph9rwi5/>

    > Would hope to see your setup and benchmark, if possible try a longer 256k context cache on a well known model with at least 32GB, better 70-90B or more (if your machine handles it).

- **CheapProg6886** · 12 分 · 2026-10-17T07:31:42 · <https://www.reddit.com/r/MacStudio/comments/1x815vj/comment/ph9il6e/>

  > M5 ultra 80c 256gb. zero buyers remorse. it’s acting like a headless server for me and i’m accessing glm 5.3 flash on it from different devices. only regret is not waiting for the 512 now.

- **ThePotentialHD** · 17 分 · 2026-10-17T04:44:37 · <https://www.reddit.com/r/MacStudio/comments/1x815vj/comment/ph8xnr6/>

  > I can come back in 3 months after my delivery window 🥲

- **trollwoke** · 16 分 · 2026-10-17T05:35:57 · <https://www.reddit.com/r/MacStudio/comments/1x815vj/comment/ph94cnz/>

  > As always if you expect it to replace a single claude max or chatgpt subscription you will be disappointed
  >
  >  If you just want to play around with local models it’s fine
  >
  >  If you want it to be an inference box for multiple people it’s the wrong tool for that job
  >
  >  As a piece of hardware it’s incredible, a brilliant workstation besides the popping and clicking noises it makes
  >
  >  Had mine 2 weeks AMA

  - **imtourist** · 13 分 · 2026-10-17T05:55:48 · <https://www.reddit.com/r/MacStudio/comments/1x815vj/comment/ph96ua1/>

    > I thought long and hard about upgrading my current 64gb M4 MAX to a 128gb M5 MAX but after looking at the performance numbers it still doesn't nearly approach the performance of an online frontier or open weight model. I figure if I sold my current M4 and bought a new M5 I would be paying about $3 or $4K more ... and with that money I could probably buy a few years of online tokens and also have better performance.
    >
    >  The truth is for my needs the M4 Max is is sufficient for long running background agentic tasks and rely on online models for more bursty tasks. Other people's requirements are different but for a lot of things its pretty hard to beat the combined heft of a H200 cluster for large models.

    - **Sketaverse** · 6 分 · 2026-10-17T07:34:24 · <https://www.reddit.com/r/MacStudio/comments/1x815vj/comment/ph9iwro/>

      > This is the right answer

  - **urza_insane** · 4 分 · 2026-10-17T06:56:21 · <https://www.reddit.com/r/MacStudio/comments/1x815vj/comment/ph9ea5x/>

    > Is the popping and clicking an actual thing?

    - **PopMany2921** · 4 分 · 2026-10-17T14:22:22 · <https://www.reddit.com/r/MacStudio/comments/1x815vj/comment/phb5bjt/>

      > It is you can hear the power equipment clicking, people say it’s good that your hear it because the parts aren’t cheap.

- **ceinewydd** · 6 分 · 2026-10-17T16:22:03 · <https://www.reddit.com/r/MacStudio/comments/1x815vj/comment/phbuykl/>

  > Nobody has an M5U 512GB and so there’s a group of people who explicitly want it for AI, but who can’t comment as real buyers until at least next month.

- **ln28909** · 2 分 · 2026-10-22T10:50:20 · <https://www.reddit.com/r/MacStudio/comments/1x815vj/comment/19rhaqsetnrno/>

  > Just received my base m5 ultra running Qwen 3.8 flash next, works well
  > Ttft: 5-30s
  > Tps: 80+ single user, 40+ 3 users
  > Qwen seems very smart, i can get all my work that was done by codex $20 plan previously without issue and much more since there is no usage limit.
  > Does a lot better for deep log reading and troubleshooting compared with codex, i tried to troubleshoot my frigate setup with codex for a couple days with minimal improvement but Qwen does a lot better

  - **redmormon** [OP] · 1 分 · 2026-10-23T08:18:58 · <https://www.reddit.com/r/MacStudio/comments/1x815vj/comment/19riw7xz9g4p1/>

    > nice, thanks for sharing, which ram model did you buy?

- **AceMcLoud27** · 4 分 · 2026-10-17T08:02:10 · <https://www.reddit.com/r/MacStudio/comments/1x815vj/comment/ph9m6q1/>

  > I regret not ordering earlier, mine arrives mid November ;-)

- **XxBrando6xX** · 3 分 · 2026-10-17T06:32:41 · <https://www.reddit.com/r/MacStudio/comments/1x815vj/comment/ph9bea8/>

  > M5 ultra 256. I think it’s pretty neato. And it does ai things real good. I run qwen flash next and qwen 3.8 27b and use them for some kind of multi agentic coding workflow guy.

- **bakawolf123** · 7 分 · 2026-10-17T08:50:25 · <https://www.reddit.com/r/MacStudio/comments/1x815vj/comment/ph9rsib/>

  > Unlike woke troll I say you absolutely replace a big cloud sub with that.
  > In fact at times I think I should even cancel my $20 one, atm using it for review or concurrency. Glm5.3-flash does the job, in many cases better than sol6.1 xhigh. Actual speed (not bench, sampling, up to 400k context) - 2.3k long prefill, 75-85 TG. While that is churning I can even play games on the same machine (perfomance dips like 10% at most).
  > Also using h3 for video gen, works well too 10s 1536x1024 clips take 10 min, 960x544 5s take 80s.
  > Energy usage is quite moderate too. The most I had it was 200W when trying some parallel video gen, but normally it is up to 185W. For llms with dflash it's 70-90W.
  > Engines: omlx for llm, vpipe for diffusion.
  >
  >  One bit regarding speed, don't take benches without a grain of salt, for the matter of fact all those 160+ scores here on glm5.3-flash are mine (as of now), yet I think I probably leave like 5tps at most on the table by using upstream and not my old fork that showed biggest numbers on dflash and mtp is usually slower overall even on upsteam despite doing that 165+ on 16k python consistently https://omlx.ai/benchmarks/performance?model=glm-5.3-flash&chip=&device=&quantization=&context=&sort=tg_tps&order=desc&pp_min=&tg_min=&memory_min=&memory_max=&hide_specprefill=1

- **snamuh** · 2 分 · 2026-10-17T06:18:19 · <https://www.reddit.com/r/MacStudio/comments/1x815vj/comment/ph99mu0/>

  > Love mine.

- **jakeliu88** · 2 分 · 2026-10-17T16:11:43 · <https://www.reddit.com/r/MacStudio/comments/1x815vj/comment/phbsnrs/>

  > It good but not worth it for the price, I bought m5 max 128gb studio can run qwen 3.8 flash next fine 70-100 token per sec (3.3 bit) and GLM 5.3 flash (2 bit) 30-40 tps . But it just not smart enough still have to pay couple $20 accounts to maintain the work I do. Can’t imagine I pay $10k for it. I think you’ll get 10% better if you have 256k for GLM 5.3 flash 4 bit model. That is not worth 5k.
