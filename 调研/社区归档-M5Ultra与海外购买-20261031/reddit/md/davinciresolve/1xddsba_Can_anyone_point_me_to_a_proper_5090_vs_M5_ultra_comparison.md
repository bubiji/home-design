# Can anyone point me to a proper 5090 vs M5 ultra comparison?

- 来源:r/davinciresolve · 作者 Legitimate-Table-607 · 2026-10-23T13:17:25 · 分数 3 · 评论 19(本页抓到 13)
- 原链接:https://www.reddit.com/r/davinciresolve/comments/1xddsba/can_anyone_point_me_to_a_proper_5090_vs_m5_ultra/

> ⚠️ 以下引用块为逐字原件,未改写。

## 正文

> Do anyone have real M5 ultra vs desktop 5090 performance figures? Not just benchmarks, real performances differences in real video editing workflows.
>
>  I have a 9950x3d, with a 5090 and 64gb of DDR5 which I built just before everything went mad and at the time Apple hadn't released anything that could really compete with the 5090. I really love the performance of the PC and for the most part just don't need to worry about performance.
>
>  The thing is, I much prefer Mac OS from a usability standpoint and the fan noise / heat of the 5090 system is quite annoying and there's always this worry in the back of my mind that my GPU is going to melt.
>
>  I'm tempted to switch over the m5 ultra, but it's hard to find real world performance differences in Resolve, I don't just mean stacking loads of 6k clips with no effects and then saying 'who would need more than this?!' like the youtubers do. I mean performance with 5k raw with NR, bit depth etc.
>
>  I checked out puget and can't see any m5 ultra entries as of yet and I do worry they're a bit biased against mac.
>
>  Thoughts? Anyone tried both?

## 评论

- **greenysmac** · 4 分 · 2026-10-23T13:53:42 · <https://www.reddit.com/r/davinciresolve/comments/1xddsba/comment/19rjb5fjfy1s5/>

  > This is about all you're see.
  >
  >  https://www.pugetsystems.com/pugetbench/results/compare/Puget%20Bench%20for%20DaVinci%20Resolve/33/GPU/NVIDIA%20GeForce%20RTX%205090/Apple%20M5%20Max(40%20Cores)/

  - **Legitimate-Table-607** [OP] · 0 分 · 2026-10-23T14:00:17 · <https://www.reddit.com/r/davinciresolve/comments/1xddsba/comment/19rjbg0c4p1mr/>

    > Yeah I saw that m5 max comparison, which is weird because it’s not that far off in a lot of areas and even faster in a select few but obviously lags being in raw gpu horsepower but obviously the m5 ultra may be much closer or even ahead?

    - **greenysmac** · 5 分 · 2026-10-23T15:07:38 · <https://www.reddit.com/r/davinciresolve/comments/1xddsba/comment/19rjeg56m8hhh/>

      > There is nobody I know who realistically has the same project pumped through both of these systems, so this is about the closest you're ever going to find in real performance here.
      >
      >  The real practical difference between the Ultras is going to be twice as many CPUS.
      >
      >  The question just becomes how much CPU specific specialization DaVinci Resolve is going to be able to take advantage of. I don't have a real straight answer for that.
      >
      >  We have to wait for the orders to hit.
      >
      >  At a secondary level, the M5s have got this new neural architecture, and it makes a huge difference for things like Magic Mask. I don't know how much the Puget system test does. If you're able to afford either, I have to go with the M5 Ultra.
      >
      >  That is especially true if there's any ProRes involved, because there are so many hardware encoder- and decoder-based ProRes chips that you get an extra, crazy powerful benefit from them on the M5 Max and even more so on an Ultra.
      >
      >  My question really becomes: is it more about cost, and does the cost difference between a specced-out 5090 with some decent RAM and an M5 Max Ultra make any real difference to your pocket??

- **gargoyle37** · 10 分 · 2026-10-23T17:09:32 · <https://www.reddit.com/r/davinciresolve/comments/1xddsba/comment/19rjjvvhf2u80/>

  > This depends on the workload. Heavily.
  >
  >  An RTX 5090 is going to run circles around the M5 in neural processing and raw 32 bit floating point compute. In equivalently priced desktop AMD system would be a Threadripper configuration, so its multi-core performance completely outpaces the M5 chip as well.
  >
  >  So if you are doing something like 3d cg rendering, there's no competition: an AMD/Nvidia system wins on price.
  >
  >  But, for video work, there's a couple of things which leans toward the M5. It has excellent single-core performance, and a lot of NLE work is inherently not that parallelizable, so this makes it pretty strong. If you care about power draw, then M5s are really strong since that's what the whole architecture are built around. Apple often touts that they are ahead of everyone in performance per watt, which isn't false. But that's just not very useful if you require peak performance.
  >
  >  I.e., the TL;DR is that it's different systems which are balanced differently in their setup. NLE work like Resolve is tricky because it falls somewhat in the middle. My guess, based on Pugets benchmarks, is that they are comparable in speed for most work in practice, unless you want to do neural processing on every frame in a 1h timeline.

  - **kidagocreative** · 1 分 · 2026-10-24T17:52:47 · <https://www.reddit.com/r/davinciresolve/comments/1xddsba/comment/19rle1ive47eo/>

    > I have the same computer but suffer through optical flow speed warp renders and ultra AI denoise nodes - usually all with 8k PR Raw. Without using those tools however, to your point, I have no complaints with the M1 Ultra. For the longest time I would brag about never needing an upgrade, but all of the latest tools are starting to age my M1 and it’s costing actual man hours

- **Qoalafied** · 4 分 · 2026-10-23T18:49:05 · <https://www.reddit.com/r/davinciresolve/comments/1xddsba/comment/19rjobpy9d18l/>

  > Specific for Resolve
  > Working a lot with graphics and fusion? 5090
  > Anything else the M5
  >
  >  I have a M1 studio thats on it’s 4th year with 6K 10bit footage. Chews any timeline of any length, up to V3 with 6k material not bogging it down. Eats h.264/65 for breakfast if you don’t go the intermidiate route.
  >
  >  Any slightly heavy fusion wil be noticable though so it’s really down to what you do most.
  >
  >  For reference I work in resolve on this mac 6 days a week and just passe shy of 900 videos created and published trough that studio.
  >
  >  Never heard the fans spin.

- **dallatorretdu** · 1 分 · 2026-10-23T19:29:09 · <https://www.reddit.com/r/davinciresolve/comments/1xddsba/comment/19rjq421623k2/>

  > If you have a 5090 pc already keep it, the fear of “if it dies” gets solved by the fact that the mac studio is readily available anyway, and that might happen when memory prices will be back to normal.
  >
  >  I was in your same situation last week and I just procrastinated it away.

- **SolidOdd4889** · 1 分 · 2026-10-25T15:42:07 · <https://www.reddit.com/r/davinciresolve/comments/1xddsba/comment/19rn0fx2tro90/>

  > your projects take over more than 32gb of video memory? if the answer is yes, even a base model mac with the memory upgraded is gonna outperform any pc. if not, save your money.
  >
  >  i switched from a 3090 to an m4 pro for this exact reason, resolve was constantly saying gpu memory full.

- **AutoModerator** · 0 分 · 2026-10-23T13:17:26 · <https://www.reddit.com/r/davinciresolve/comments/1xddsba/comment/19rj9j6pt54si/>

  > Looks like you're asking for help! Please check to make sure you've included the following information. Edit your post (or leave a top-level comment) if you haven't included this information.
  >
  >  System specs - macOS Windows - Speccy 
  >
  >  Resolve version number and Free/Studio - DaVinci Resolve>About DaVinci Resolve... 
  >
  >  Footage specs - MediaInfo - please include the "Text" view of the file.
  >
  >  Full Resolve UI Screenshot - if applicable. Make sure any relevant settings are included in the screenshot. Please do not crop the screenshot!
  >
  >  Once your question has been answered, change the flair to "Solved" so other people can reference the thread if they've got similar issues.
  >
  >  I am a bot, and this action was performed automatically. Please contact the moderators of this subreddit if you have any questions or concerns.

- **rorowhat** · -4 分 · 2026-10-23T13:54:23 · <https://www.reddit.com/r/davinciresolve/comments/1xddsba/comment/19rjb6jai0vb5/>

  > Stick to Nvidia

  - **Legitimate-Table-607** [OP] · 4 分 · 2026-10-23T13:58:49 · <https://www.reddit.com/r/davinciresolve/comments/1xddsba/comment/19rjbdmxuwvb8/>

    > What makes you say that?

    - **rorowhat** · -9 分 · 2026-10-23T14:10:57 · <https://www.reddit.com/r/davinciresolve/comments/1xddsba/comment/19rjbx4q8xhts/>

      > The ecosystem, everything being built is on Nvidia, with AMD second behind. Apple has nothing aside from overpriced consumer hardware. If you want the best support, best optimization Nvidia will get it first.

- **RetroOne_** · -4 分 · 2026-10-23T14:04:35 · <https://www.reddit.com/r/davinciresolve/comments/1xddsba/comment/19rjbmwwlp1fm/>

  > Use ChatGPT :)
