# M5 Ultra Returned to Apple

- 来源:r/MacStudio · 作者 lebante · 2026-10-14T11:17:30 · 分数 46 · 评论 33(本页抓到 24)
- 原链接:https://www.reddit.com/r/MacStudio/comments/1x5oj70/m5_ultra_returned_to_apple/

> ⚠️ 以下引用块为逐字原件,未改写。

## 正文

> English isn't my native language, so I'm translating this with DeepL and ChatGPT has helped me draft the more technical parts. An M5 Ultra 30/64 with 256 GB and 2 TB, picked up on the 1st of this month.
>
>  A few days ago, I found it turned off. When I restarted it, it displayed a “Kernel Panic” warning and a request to submit a report to Apple. After researching with ChatGPT Work and several days of testing and observation, I’ve decided to return it. The Mac has experienced severe system crashes (kernel panics) and has logged recurring errors with Apple’s graphics driver (IOGPUFamily), related to GPU memory management. Among the errors logged are IOGPUCommandDescriptor::prepare and preparedBytes != requiredBytes. These errors also appear in connection with macOS-native processes, such as mediaanalysisd, and are not limited to third-party applications. I ran Apple Diagnostics, which did not detect any hardware issues. However, the graphics driver errors continue to appear. The errors were much more frequent when using Ollama 0.40.3. My Mac mini M4 hasn’t shown any errors. I requested a return today and dropped off the package at the shipping agency.
>
>  It could be a firmware or macOS issue, but I’ve decided not to take any chances. I’ve already ordered another one with the same configuration. Estimated delivery date: December 9. If it has the same issues, I’ll assume it’s a firmware or macOS problem, but if I keep this one, I won’t feel at ease.
>
>  Edit:
>
>  log show --last 24h --style compact 
> --predicate 'process == "kernel" AND ( eventMessage CONTAINS[c] "preparedBytes != requiredBytes" OR eventMessage CONTAINS[c] "IOGPUCommandDescriptor::prepare" OR eventMessage CONTAINS[c] "failed to create resource" )' 2>/dev/null
>
>  For anyone with an M5 Ultra, it would be interesting to check whether your system logs contain similar IOGPUFamily errors. The command above is read-only and searches the last 24 hours of kernel logs. I'm particularly interested in occurrences of IOGPUCommandDescriptor::prepare and preparedBytes != requiredBytes, even if the machine hasn't experienced a kernel panic. Please include your macOS version and whether you're running MLX, Ollama or llama.cpp. I'm trying to determine whether this was an isolated hardware issue or a more widespread macOS/Metal problem.
>
>  Thanks

## 评论

- **cipher-neo** · 41 分 · 2026-10-14T11:49:15 · <https://www.reddit.com/r/MacStudio/comments/1x5oj70/comment/pgo6sbn/>

  > I’ve had the same Ultra configuration since the 9/22 launch day, running 24x7 without sleep and have not seen any of your issues. If your Ultra was running the latest macOS 27 I would say your issues were most likely HW-related. I think it was a good call to send it back.

  - **retsof81** · 1 分 · 2026-10-14T17:34:30 · <https://www.reddit.com/r/MacStudio/comments/1x5oj70/comment/pgqbyf1/>

    > Yep, no exceptions for the premium Apple charges.
    > To Apple, do better. You charge too much for this type of experience.

    - **0DarkFreezing** · 7 分 · 2026-10-14T17:49:29 · <https://www.reddit.com/r/MacStudio/comments/1x5oj70/comment/pgqfnsj/>

      > Defects happen for all manufacturers. It’s rare for Apple, but still happens.

- **paulsande** · 9 分 · 2026-10-14T11:36:01 · <https://www.reddit.com/r/MacStudio/comments/1x5oj70/comment/pgo4mih/>

  > Good choice.
  >
  >  A long time ago I had a MacBook Pro that kept having kernel panics. I should have returned it. In hindsight it must have been a hardware issue and I lived with it. So dumb.
  >
  >  I think it’s rare, but it does happen.

  - **Emotional_Banana3059** · 6 分 · 2026-10-14T12:01:16 · <https://www.reddit.com/r/MacStudio/comments/1x5oj70/comment/pgo8uc5/>

    > love the colonel panics

    - **Sneezlebee** · 3 分 · 2026-10-14T12:04:28 · <https://www.reddit.com/r/MacStudio/comments/1x5oj70/comment/pgo9eam/>

      > Ok, but show some respect and capitalize the man’s name. Colonel Panic is a national hero.

- **JDad67** · 8 分 · 2026-10-14T12:23:10 · <https://www.reddit.com/r/MacStudio/comments/1x5oj70/comment/pgocrn4/>

  > Bad machines happen. Even with apple’s QA

- **randallphoto** · 1 分 · 2026-10-15T02:35:25 · <https://www.reddit.com/r/MacStudio/comments/1x5oj70/comment/pgtl1x2/>

  > Does your kernel panic mention WindowServer at all?

  - **lebante** [OP] · 1 分 · 2026-10-15T21:33:43 · <https://www.reddit.com/r/MacStudio/comments/1x5oj70/comment/pgzhyfh/>

    > I can't find the report; I deleted the original when I reset the Mac, but I don't recall it being mentioned. The kernel panic was a watchdog timeout.

    - **randallphoto** · 1 分 · 2026-10-15T21:44:27 · <https://www.reddit.com/r/MacStudio/comments/1x5oj70/comment/pgzk9e9/>

      > It’s highly likely related. My kernel panic report was a watchdog timeout for windowserver. Setting your display to 60hz (and if you have multiple displays setting them all to 60hz) helped a lot for me

- **BlueberryValuable653** · 1 分 · 2026-10-14T12:22:16 · <https://www.reddit.com/r/MacStudio/comments/1x5oj70/comment/pgoclml/>

  > You’re hitting out of memory issues. What models are you running.
  >
  >  Do you have the panic string for your kernel panics. Did you report it to Apple and forward the panic information?

  - **lebante** [OP] · 1 分 · 2026-10-14T12:39:44 · <https://www.reddit.com/r/MacStudio/comments/1x5oj70/comment/pgofwnq/>

    > Yes, i did. The machine had 256GB of unified memory, so I wouldn't expect the 27B model to cause OOM issues. Also, some of the same GPU errors showed up in Apple's own mediaanalysisd process, even without running an LLM.

    - **BlueberryValuable653** · -1 分 · 2026-10-14T12:51:48 · <https://www.reddit.com/r/MacStudio/comments/1x5oj70/comment/pgoi8nv/>

      > That doesn’t get around the fact that you are getting out of memory issues. Without knowing your memory load, what you’ve twiddled like what llama.cop documents, it’s hard to really say.
      >
      >  But those errors are purely out of memory issues.

  - **pray4bigsurf** · 0 分 · 2026-10-14T12:55:04 · <https://www.reddit.com/r/MacStudio/comments/1x5oj70/comment/pgoiw0f/>

    > Personally had this happen on an m5 max 64GB (Qwen 3.8 27B Q8 mlx variant) at about half context. Looked like iogpu but ended up seeming like the kv grew unbounded beyond the set limit and deadlocked and completely maxed out ram. Kernel watchdog fired at 90 seconds and reboot took place. Doesn't happen with gguf variant.

- **Ascetic-anise** · 2 分 · 2026-10-16T09:43:14 · <https://www.reddit.com/r/MacStudio/comments/1x5oj70/comment/ph2s2wy/>

  > I have an M2 Ultra 128GB, bought it about 3 years ago. A month before my Apple Care was about to expire it started to have some bizarre application crashes. Then, the Mac Studio reset twice by itself on the same week. Running the Apple hardware tests confirmed a memory issue and recommended that I bring it back for servicing. I dropped it at the Apple Store 3 days before the 3 years Apple Care expiry. Needless to say, I have enrolled it to the yearly Apple Care.

  - **ShrimpCocktail-4618** · 1 分 · 2026-10-16T21:04:26 · <https://www.reddit.com/r/MacStudio/comments/1x5oj70/comment/ph6qg1q/>

    > Good thing you added AppleCare. Even though you shouldn't have to do the warranty on a high end product, on Apple gear, especially, you can get kicked in the nuts with repair charges without it. With it, they can be minor fees. They may even replace whole parts.

- **Ascetic-anise** · 2 分 · 2026-10-16T09:44:45 · <https://www.reddit.com/r/MacStudio/comments/1x5oj70/comment/ph2s9rt/>

  > General note to people, if you machine is having a memory issue it may crash and the process that crashes doesn’t matter

- **RyanElectrified** · 3 分 · 2026-10-14T13:57:14 · <https://www.reddit.com/r/MacStudio/comments/1x5oj70/comment/pgovxrf/>

  > You remind me I had similar issues with my original M1 Macbook Air, but I swapped it out and the replacement was perfect. Sometimes a machine is bad.

- **skappley** · 1 分 · 2026-10-16T08:17:48 · <https://www.reddit.com/r/MacStudio/comments/1x5oj70/comment/ph2hskt/>

  > I have an M5U with 96GB of RAM, got it on Sept. 23rd. It didn't have any crashes or kernel panics, but I see entries like this one in the logs (checked with your command):
  >
  > 2026-10-16 08:12:53.892 F kernel[0:4bd689] (IOGPUFamily) virtual IOReturn IOGPUCommandDescriptor::prepare(uint32_t) <mediaanalysisd>: preparedBytes != requiredBytes : preparedBytes = <27148288> requiredBytes = <21381120> maxWired = <83494174720> preWiring = <3401367552> currentWired = <3409821696> wiring delta = <8454144>

- **rypher** · 0 分 · 2026-10-14T11:23:43 · <https://www.reddit.com/r/MacStudio/comments/1x5oj70/comment/pgo2nui/>

  > Interesting, same specs I ordered. Hopefully its just a lemon. (Not a wide-spread issue)

  - **tk421tech** · 1 分 · 2026-10-14T11:51:51 · <https://www.reddit.com/r/MacStudio/comments/1x5oj70/comment/pgo786b/>

    > I have the same one, have not experienced any issues but right now I have only been migrating files and setting up programs.

- **idmimagineering** · 0 分 · 2026-10-14T18:31:27 · <https://www.reddit.com/r/MacStudio/comments/1x5oj70/comment/pgqq3qx/>

  > We had 3 2020 iMacs that were shyte.
  > Constant deep sleep or boot to black.
  > Tahoe 26.7.1 fixed them :-O

  - **jah-roole** · 1 分 · 2026-10-16T17:53:28 · <https://www.reddit.com/r/MacStudio/comments/1x5oj70/comment/ph5ip4k/>

    > Vat?

  - **Dependent_Chard_8393** · 1 分 · 2026-10-14T20:01:27 · <https://www.reddit.com/r/MacStudio/comments/1x5oj70/comment/pgrc26v/>

    > Any ideas why LM Studio makes it behave that way?
