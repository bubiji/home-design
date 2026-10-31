# M5 Max 128GB vs M5 Ultra 256GB – DaVinci Resolve Performance

- 来源:r/colorists · 作者 Accomplished_Ad_6403 · 2026-10-19T10:02:45 · 分数 2 · 评论 14(本页抓到 10)
- 原链接:https://www.reddit.com/r/colorists/comments/1x9stkh/m5_max_128gb_vs_m5_ultra_256gb_davinci_resolve/

> ⚠️ 以下引用块为逐字原件,未改写。

## 正文

> Hello everyone!
>
>  I’m considering moving to Apple Silicon and would appreciate some real-world feedback.
>
>  My workflow mainly involves:
> Up to 8K footage (ProRes RAW and other high-resolution formats)
> Heavy temporal noise reduction (Neat Video)
> Magic Mask, Depth Map and Relight
> Multiple nodes with CSTs and secondary corrections
> 1080p/4K timelines with render caching
>
>  I’m considering an M5 Max with 128GB unified memory versus an M5 Ultra with 256GB.
>
>  My biggest concern is GPU performance, particularly with multiple Resolve FX enabled simultaneously.
>
>  For anyone using either machine professionally, how does playback, scrubbing and rendering perform with these effects?
> Would the M5 Max be sufficient, or is the Ultra worth the additional investment?
>
>  Thanks in advance!

## 评论

- **joema2** · 6 分 · 2026-10-19T15:37:34 · <https://www.reddit.com/r/colorists/comments/1x9stkh/comment/phppr9i/>

  > If you use temporal/spatial noise reduction (TSNR), Neat Video, Magic Mask, Depth Map, and Relight on up to 8k material, it will be slow on any machine, even a top-spec M5 Ultra or a PC workstation with a 32 GB RTX-5090. And the 32 GB 5090 is about $5k all by itself.
  >
  >  Those are generally multi-frame or "temporal" effects that *each* operate on a sliding window of frames. For each frame in the window, other upstream effects must often be recomputed. When using several temporal effects, the performance cost can be exponential -- on any machine, using any GPU.
  >
  >  The best practice is:
  >
  >  - Defer using such effects until later in the edit phase. Don't put them on during the edit "just to make it look good."
  >
  >  - Do not apply them to the base clip. Apply them only to the final edited clip. E.g, if you are using 10 seconds from a 5-minute interview, don't apply them to all 5 min. Wait until the edit is nearly finished and apply them to the 10 seconds of that interview clip.
  >
  >  - Consider "baking in" certain temporal effects. E.g, for TSNR or Neat Video, apply those, export the clip to ProRes 422 or DNx, import and replace.
  >
  >  - If you need a "pretty" demo for a producer, tightly select a limited number of good-looking short clips, possibly transcode those to 1080p, put them on a timeline, apply and tweak the effects for the best look, then export. That would be a separate effort. Don't get bogged down trying to produce such a thing using 8k clips and multiple temporal effects.
  >
  >  In general, for those types of effects, the GPU scaling is pretty good. Not linear, but useful. An easy way to examine that is using the command-line Neat Video benchmark neatbench6, which can be downloaded from here: https://www.neatvideo.com/download/neatbench
  >
  >  Below are the GPU and combined CPU+GPU UHD/4k numbers from my M1 Max MacBook Pro 16 vs my M1 Ultra Mac Studio. In this case the M1 Ultra GPU with 2x the GPU cores was about 1.8x faster than the M1 Max. But that is only *one* effect. There is no machine in existence that can smoothly run multiple temporal effects of this type on 8k clips in an uncached timeline with smooth performance.
  >
  >  So all the YouTubers who comment, "Who could possibly need this level of performance," are indicating they have never done work like this and are unfamiliar with it.
  >
  >  M1 Ultra:
  > GPU (Apple M1 Ultra): 16.81 frames/sec
  > CPU (19 cores) and GPU (Apple M1 Ultra): 23.39 frames/sec
  >
  >  M1 Max:
  > GPU (Apple M1 Max): 9.37 frames/sec
  > CPU ( 9 cores) and GPU (Apple M1 Max): 14.31 frames/sec

  - **Accomplished_Ad_6403** [OP] · 1 分 · 2026-10-19T15:43:49 · <https://www.reddit.com/r/colorists/comments/1x9stkh/comment/phpr8lx/>

    > Hello Joema!
    >
    >  Thank you! I was previously running a rtx pro 6000 and yes you’re right, it still does need to render cache for smooth playback, however I think it’s still overkilling it for what it is and am looking for a middle ground, was wondering in your opinion, would a ultra 96gb or 256gb be enough?

    - **joema2** · 2 分 · 2026-10-19T15:55:32 · <https://www.reddit.com/r/colorists/comments/1x9stkh/comment/phpu0tm/>

      > I'll let you know in about four weeks when I receive my 256 GB M5 Ultra.

- **greenysmac** · 6 分 · 2026-10-19T11:28:21 · <https://www.reddit.com/r/colorists/comments/1x9stkh/comment/phobiwd/>

  > Ultra is worth it for the extra cycles especially with the variety of effects you're using.
  >
  >  Easiest general item is to look at performance on PugetSystems - but there's no way to separate GPU from CPU.

- **PsychologicalSlip641** · 2 分 · 2026-10-25T11:30:57 · <https://www.reddit.com/r/colorists/comments/1x9stkh/comment/19rmp8mw5mqg2/>

  > Sounds like none of the above model are enough to compute everything at once in livetime…

- **Intrepid-Try-3430** · 1 分 · 2026-10-22T14:02:16 · <https://www.reddit.com/r/colorists/comments/1x9stkh/comment/19rhjazm1f5ur/>

  > Hey! I have an M5 Max MacBook Pro with 64GB of RAM, and it handles 6K RED RAW footage on a 4K timeline smoothly, even with Depth Map, Magic Mask, and noise reduction applied, using Smart Cache.
  > If you’re considering a desktop setup, I think an M5 Ultra or a system with an RTX 5090 would be ideal for your needs! :)

- **DegreeSevere7719** · 1 分 · 2026-10-19T13:15:27 · <https://www.reddit.com/r/colorists/comments/1x9stkh/comment/phoudgk/>

  > Ultra will be better, but not as much as the price difference. GPU compute will still be the weak point compared to nvidia offerings, but with today's prices - moving even to ultra mac does make financial sense. For some realistic workflow on M5 Max - watch this video: https://www.youtube.com/watch?v=7RIdwr8NlKo

  - **joema2** · 2 分 · 2026-10-20T15:48:46 · <https://www.reddit.com/r/colorists/comments/1x9stkh/comment/phwrev1/>

    > The latest Puget Resolve 2.0 benchmarks do not show a major GPU weakness in the M5 Ultra vs RTX-5090 when running a representative effects-heavy Resolve workload mix. To my knowledge, no reviewer thus far has done a methodical comparison, so I downloaded all available data from the Puget database and analyzed it.
    >
    >  There are only seven M5 Ultra submissions so far, but comparing those to the 33 recent RTX-5090 uploads shows interesting results. In general, the M5 Ultra is faster overall, but as the fraction of GPU-intensive effects increases (Puget Basic vs Standard vs Extended test), the RTX-5090 systems improve. But as a group they are only 2% faster than the M5 Ultra on the GPU-intensive "Extended" test. On the Basic and Standard test, the M5 Ultra is faster. See attached.

    - **DegreeSevere7719** · -1 分 · 2026-10-20T16:14:05 · <https://www.reddit.com/r/colorists/comments/1x9stkh/comment/phwwerh/>

      > I wouldn't take Pudget as a good reference point on the GPU compute. Look through their tasks and compare it to the real workloads today, and you'll understand that it just doesn't test anything near modern workflows - no codecs, no tools, no plug-ins. To me, T2F benchmark is way more representative for modern workloads, because, at least, it does use some of the modern footage, resolutions and tools inside Resolve. But I digress, it's best to test gear on your own projects - often times stuff hitting high on benchmarks - will work slow for your own stuff, and that's exactly the reason I'm saying apple silicon is still lacking on gpu compute - it's my own experience of working with it on raw footage with stuff like AI Facemasks, NR, tracking etc. I'm pretty certain it will be just enough and will work fine (both the M5max and M5Ultra), but, in stuff where the gpu brute force is needed - it will perform 1/2 to 1/3 of the 5090 or dual 5080 slim setup. However, in today's market, and considering the reliability issues with 5090s - I think going with m5max or m5ultra might be a wise and weighted decision.

- **llambdaddy** · 1 分 · 2026-10-19T21:20:53 · <https://www.reddit.com/r/colorists/comments/1x9stkh/comment/phrzz4a/>

  > These systems are more designed around running ai models than high-performance creative tasks. They’re also priced to those markets, too. They’re much more memory-rich than compute-rich. Especially when it comes to GPU performance. But I can imagine there isn’t much incentivising Apple to push their GPU compute when a lot more revenue is coming from ai projects clustering these units together over TB5.
