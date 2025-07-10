---
layout: post
permalink: /
title: Java Garbage Collector (Insights & Experiments)
post: 2473811668075049989
labels: Java, JVM, GC
---

<img src="imgs/gc_cover.jpeg" height="320px" width="100%" />

## Introduction

I thought of trying out all types of Garbage Collectors in Java and decided to see how they behave in different scenarios. Creating one piece of code to see them in action wasn't possible for me, thus I thought of starting with sample program first to know whether switching garbage collector actually is working or not.

There are different types of garbage collectors in java, listing them below:
- Serial
- Parallel
- CMS (Concurrent Mark-Sweep)
- G1 (Garbage First)
- ZGC (Z Garbage Collector)
- Shenandoah

For given java program (or application) I can switch to any given garbage collector using JVM option; `-XX:+UseXYZGC`. 

## Know Which GC 
But I wanted to print it in my program execution; just to see which GC is in action. I came across `java.lang.management` which has required information that I needed to confirm which garbage collector is in use. 

In this API `ManagementFactory.getGarbageCollectorMXBeans()` returns all MX (Management Extension) Beans for the chosen Garbage Collectors. Note that from Java 9+ default garbage collectro is Z1.

```java
List<GarbageCollectorMXBean> gcBeans = ManagementFactory.getGarbageCollectorMXBeans();
```

I created a method printing this bean names for each garbage collector; I was using Open JDK 21.

```java
private void whichGC() {
    List<GarbageCollectorMXBean> gcBeans = ManagementFactory.getGarbageCollectorMXBeans();
    Set<String> names = new HashSet<>();
    for (GarbageCollectorMXBean gc : gcBeans) {
        names.add(gc.getName());
    }
    System.out.println(names);
}
```

For each GC following is what I got in Output:
- Serial: `[Copy, MarkSweepCompact]`
- Parallel: `[PS MarkSweep, PS Scavenge]`
- CMS: **Deprecated!** - Got runtime error `Unrecognized VM option 'UseConcMarkSweepGC'`
- G1: `[G1 Young Generation, G1 Old Generation, G1 Concurrent GC]`
- ZGC: `[ZGC Pauses, ZGC Cycles]`
- Shenandoah: `[Shenandoah Cycles, Shenandoah Pauses]`

I modified my method a bit to get the name of Garbage collector.

```java
private String whichGC() {
    List<GarbageCollectorMXBean> gcBeans = ManagementFactory.getGarbageCollectorMXBeans();
    
    if(!gcBeans.isEmpty()) {
        String gcPrefix = gcBeans.get(0).getName().split(" ")[0];

        switch (gcPrefix) {
            case "Copy": return "Serial Garbage Collector";
            case "PS": return "Parallel Garbage Collector";
            case "G1": return "Garbage First - G1  Garbage Collector";
            case "ZGC": return "Z Garbage Collector";
            case "Shenandoah": return "Shenandoah Garbage Collector";
        }
    }
    
    return "Unknown";
}
```

## Serial GC Play
I thought of exploiting Serial GC to see what are it's limitation that Parallel GC can overcome. 

Few basic things I knew about Serial GC,
- Single Threaded
- Not Parallel (This is obvious; _thus name Serial_)
- Pauses the application threads

I want to see when and how garbage collection occurs; I came across two JVM options which can print garbage collector events.
- `-XX:+PrintGC`: Prints GC event basic details
- `-XX:+PrintGCDetails`: Prints GC details

... but later realised both are deprecated in Java 9 and replaced by `-Xlog:gc` which is much flexible and highly configurable JVM option. Realising I don't need `java.lang.management` for printing GC this logs itself starts with the name of GC. But there has lot to explore in management API for sure.


I thought of creating a simple program to see this GC doing something; but garbage collector will do clean up (_automatically_) in one of the following cases,
- Not enough free memory in heap
- Eden space is full (Young Generation)
- When long lived objects fill the Old Generation
- `System.gc()` is called
- Based on allocation rate of heap usage thresolds configuration
- etc. 

So, I have many options that I can trigger the garbage collection. I decided to go with memory trigger.

To keep the heap memory lower and occupying memory faster I created following program,

```java
public class TrySerialGC {

    public static void main(String[] args) throws InterruptedException {
        for(int i = 0; i < 30; i++) {
            byte[] b = new byte[5 * 1024 * 1024];
            System.out.println("5 MB Allocated");
            Thread.sleep(1000);
        }
    }
}
```

I ran this program in following way,

```shell
javac TrySerialGC.java
java -XX:+UseSerialGC -Xmx64m -Xms64m -Xlog:gc TrySerialGC
```

The output was bit confusing, If I'm allocating 64 MB to heap and creating `byte[]` array of size 5 MB 30 times which ideally mean objects of 150 MB in a loop. However, the GC event log was triggered 10 times.

```shell
[0.012s][info][gc] Using Serial
5 MB Allocated
5 MB Allocated
[2.212s][info][gc] GC(0) Pause Young (Allocation Failure) 14M->1M(61M) 3.074ms
5 MB Allocated
5 MB Allocated
5 MB Allocated
[5.227s][info][gc] GC(1) Pause Young (Allocation Failure) 17M->1M(61M) 2.265ms
5 MB Allocated
5 MB Allocated
5 MB Allocated
[8.239s][info][gc] GC(2) Pause Young (Allocation Failure) 16M->1M(61M) 1.367ms
5 MB Allocated
5 MB Allocated
5 MB Allocated
[11.249s][info][gc] GC(3) Pause Young (Allocation Failure) 16M->1M(61M) 1.793ms
5 MB Allocated
5 MB Allocated
5 MB Allocated
[14.262s][info][gc] GC(4) Pause Young (Allocation Failure) 16M->1M(61M) 1.795ms
5 MB Allocated
5 MB Allocated
5 MB Allocated
[17.278s][info][gc] GC(5) Pause Young (Allocation Failure) 16M->1M(61M) 1.794ms
5 MB Allocated
5 MB Allocated
5 MB Allocated
[20.291s][info][gc] GC(6) Pause Young (Allocation Failure) 16M->1M(61M) 1.601ms
5 MB Allocated
5 MB Allocated
5 MB Allocated
[23.302s][info][gc] GC(7) Pause Young (Allocation Failure) 16M->1M(61M) 1.792ms
5 MB Allocated
5 MB Allocated
5 MB Allocated
[26.312s][info][gc] GC(8) Pause Young (Allocation Failure) 16M->1M(61M) 1.795ms
5 MB Allocated
5 MB Allocated
5 MB Allocated
[29.322s][info][gc] GC(9) Pause Young (Allocation Failure) 16M->1M(61M) 1.839ms
5 MB Allocated
```

Actually the heap even if we allocated 64 MB; does not fully used for this allocation it is divided in to multiple parts, majorly old and young generation space. Here the young generation would usually have ~1/4 of the total space which is 16 MB, and thus after every third 5 MB allocation it is performing garbage collection.

Due to JVM warm up, there are several short lived objects used young generation space and reduces space for us to allocate for our `byte[]` object and thus we can see the GC takes place after two objects are created and occupied space is 14 MB so third 5 MB allocation is not possible. However, after garbage collection JVM reclaims young generation and now there is more space 16-17MB to allocate three objects before next garbage collection.

It's important to decode the log now what each part conveys,

```shell
[2.212s][info][gc] GC(0) Pause Young (Allocation Failure) 14M->1M(61M) 3.074ms
```

- `[2.212s]` : The GC event occurred `2.212s` seconds after the JVM started.
- `[info][gc] GC(0)` : Log type and `GC(0)` means GC event number 0
- `Pause Young (Allocation Failure)`: Reason of GC which is `Allocation Failure` and happened for which generation; stating the application threads were paused for the garbage collection.
- `14M->1M(61M)` : `14 MB` was the size of occupied young generation which braught down to `1MB` after garbage collection. `61 MB` is total young and old generation space; `3 MB` is space reserved for internal bookeeping, buffers, metadata etc.
- `3.074ms` : Time taken for garbage collection.


## Paralle GC Play
Parallel GC internally uses multiple worker threads to perform the garbage collection which is faster than Serial GC. Thus I tried the same program with Parallel garbage collector option and got following output,

```shell
[0.011s][info][gc] Using Parallel
5 MB Allocated
5 MB Allocated
[2.179s][info][gc] GC(0) Pause Young (Allocation Failure) 13M->1M(61M) 4.725ms
5 MB Allocated
5 MB Allocated
5 MB Allocated
[5.189s][info][gc] GC(1) Pause Young (Allocation Failure) 16M->1M(61M) 0.844ms
5 MB Allocated
5 MB Allocated
5 MB Allocated
[8.205s][info][gc] GC(2) Pause Young (Allocation Failure) 16M->1M(61M) 1.185ms
5 MB Allocated
5 MB Allocated
5 MB Allocated
[11.219s][info][gc] GC(3) Pause Young (Allocation Failure) 16M->1M(61M) 1.166ms
5 MB Allocated
5 MB Allocated
5 MB Allocated
[14.226s][info][gc] GC(4) Pause Young (Allocation Failure) 16M->1M(61M) 1.186ms
5 MB Allocated
5 MB Allocated
5 MB Allocated
[17.236s][info][gc] GC(5) Pause Young (Allocation Failure) 16M->1M(63M) 1.344ms
5 MB Allocated
5 MB Allocated
5 MB Allocated
[20.249s][info][gc] GC(6) Pause Young (Allocation Failure) 16M->1M(63M) 0.851ms
5 MB Allocated
5 MB Allocated
5 MB Allocated
[23.262s][info][gc] GC(7) Pause Young (Allocation Failure) 16M->1M(62M) 0.281ms
5 MB Allocated
5 MB Allocated
5 MB Allocated
[26.275s][info][gc] GC(8) Pause Young (Allocation Failure) 16M->1M(63M) 0.208ms
5 MB Allocated
5 MB Allocated
5 MB Allocated
[29.282s][info][gc] GC(9) Pause Young (Allocation Failure) 16M->1M(63M) 0.266ms
5 MB Allocated
```

Which is pretty same as we are not taking any benefit of parallelism here; our program is single threaded and the allocation is linear. So, instead of doing linear allocation I divided task into 6 threads each allocating 5 objects of 5 MB each. 

```java
public class TryParallelGC {

    public static void main(String[] args) {
        Runnable runnable = () -> {
            for(int i = 0; i < 5; i++) {
                byte[] b = new byte[5 * 1024 * 1024];
                System.out.println("5 MB Allocated");
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    throw new RuntimeException(e);
                }
            }
        };

        new Thread(runnable).start();
        new Thread(runnable).start();
        new Thread(runnable).start();
        new Thread(runnable).start();
        new Thread(runnable).start();
        new Thread(runnable).start();
    }
}
```

And the output was,

```shell
[0.015s][info][gc] Using Parallel
[0.170s][info][gc] GC(0) Pause Young (Allocation Failure) 14M->11M(61M) 6.206ms
5 MB Allocated
[0.181s][info][gc] GC(1) Pause Young (Allocation Failure) 27M->26M(61M) 7.115ms
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
[1.189s][info][gc] GC(2) Pause Young (Allocation Failure) 37M->31M(61M) 4.788ms
5 MB Allocated
[1.198s][info][gc] GC(3) Pause Full (Ergonomics) 46M->21M(61M) 7.139ms
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
[2.207s][info][gc] GC(4) Pause Young (Allocation Failure) 37M->36M(61M) 5.824ms
[2.213s][info][gc] GC(5) Pause Full (Ergonomics) 51M->21M(61M) 5.108ms
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
[3.220s][info][gc] GC(6) Pause Young (Allocation Failure) 36M->26M(61M) 1.788ms
[3.225s][info][gc] GC(7) Pause Young (Allocation Failure) 41M->41M(63M) 4.983ms
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
[4.239s][info][gc] GC(8) Pause Full (Ergonomics) 56M->6M(63M) 8.215ms
[4.241s][info][gc] GC(9) Pause Young (Allocation Failure) 21M->21M(63M) 1.703ms
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
```

Something weird happened, I noticed GC kicked in immediately! may be because all threads started at the exact same time and the young generation got filled up quickly.

Interestingly, output showed `Pause Full (Ergonomics)` which is nothing but a full garbage collection and `Ergonomics` says that JVM itself decided to run full GC and not through and external trigger like `System.gc()`. Looks like, JVM couldn't clear enough memory via Young GC, so it promoted too many objects to Old Gen. Eventually, Old Gen fills up which finally triggered Full GC. 

Magically the heap size changed from 61MB to 63MB reaching towards the end of program; I had no clue what was happening. I beleive the GC reclaimed some space that was being utilised for internal purpose like bookeeping, metadata etc. But I was wrong the remaining 1–3 MB difference is usually survivor space tweaks, alignment padding, or growth of the old gen. To dive deeper I ran the same program with `-Xlog:gc,gc+heap=info,gc+age=debug` and the output was following,


```shell
[0.011s][info][gc] Using Parallel
[0.126s][info][gc,heap] GC(0) PSYoungGen: 13845K(18944K)->624K(18944K) Eden: 13845K(16384K)->0K(16384K) From: 0K(2560K)->624K(2560K)
[0.126s][info][gc,heap] GC(0) ParOldGen: 1055K(44032K)->11303K(44032K)
[0.126s][info][gc     ] GC(0) Pause Young (Allocation Failure) 14M->11M(61M) 7.389ms
[0.139s][info][gc,heap] GC(1) PSYoungGen: 17008K(18944K)->720K(18944K) Eden: 16384K(16384K)->0K(16384K) From: 624K(2560K)->720K(2560K)
[0.139s][info][gc,heap] GC(1) ParOldGen: 11303K(44032K)->26672K(44032K)
[0.139s][info][gc     ] GC(1) Pause Young (Allocation Failure) 27M->26M(61M) 9.185ms
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
[1.146s][info][gc,heap] GC(2) PSYoungGen: 12138K(18944K)->624K(18944K) Eden: 11418K(16384K)->0K(16384K) From: 720K(2560K)->624K(2560K)
[1.146s][info][gc,heap] GC(2) ParOldGen: 26672K(44032K)->31800K(44032K)
[1.146s][info][gc     ] GC(2) Pause Young (Allocation Failure) 37M->31M(61M) 4.947ms
5 MB Allocated
[1.154s][info][gc,heap] GC(3) PSYoungGen: 16193K(18944K)->0K(18944K) Eden: 15569K(16384K)->0K(16384K) From: 624K(2560K)->0K(2560K)
[1.154s][info][gc,heap] GC(3) ParOldGen: 31800K(44032K)->21948K(44032K)
[1.154s][info][gc     ] GC(3) Pause Full (Ergonomics) 46M->21M(61M) 6.985ms
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
[2.160s][info][gc,heap] GC(4) PSYoungGen: 16199K(18944K)->96K(18944K) Eden: 16199K(16384K)->0K(16384K) From: 0K(2560K)->96K(2560K)
[2.160s][info][gc,heap] GC(4) ParOldGen: 21948K(44032K)->27068K(44032K)
[2.160s][info][gc     ] GC(4) Pause Young (Allocation Failure) 37M->26M(61M) 2.036ms
[2.166s][info][gc,heap] GC(5) PSYoungGen: 15456K(18944K)->96K(20480K) Eden: 15360K(16384K)->0K(17920K) From: 96K(2560K)->96K(2560K)
[2.166s][info][gc,heap] GC(5) ParOldGen: 27068K(44032K)->42428K(44032K)
[2.166s][info][gc     ] GC(5) Pause Young (Allocation Failure) 41M->41M(63M) 6.070ms
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
[3.176s][info][gc,heap] GC(6) PSYoungGen: 16015K(20480K)->0K(18944K) Eden: 15919K(17920K)->0K(17920K) From: 96K(2560K)->0K(1024K)
[3.176s][info][gc,heap] GC(6) ParOldGen: 42428K(44032K)->6587K(44032K)
[3.176s][info][gc     ] GC(6) Pause Full (Ergonomics) 57M->6M(61M) 5.726ms
[3.178s][info][gc,heap] GC(7) PSYoungGen: 15360K(18944K)->0K(20480K) Eden: 15360K(17920K)->0K(19456K) From: 0K(1024K)->0K(1024K)
[3.178s][info][gc,heap] GC(7) ParOldGen: 6587K(44032K)->21947K(44032K)
[3.178s][info][gc     ] GC(7) Pause Young (Allocation Failure) 21M->21M(63M) 1.811ms
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
[4.181s][info][gc,heap] GC(8) PSYoungGen: 15842K(20480K)->64K(20480K) Eden: 15842K(19456K)->0K(19456K) From: 0K(1024K)->64K(1024K)
[4.181s][info][gc,heap] GC(8) ParOldGen: 21947K(44032K)->27067K(44032K)
[4.181s][info][gc     ] GC(8) Pause Young (Allocation Failure) 36M->26M(63M) 1.748ms
[4.183s][info][gc,heap] GC(9) PSYoungGen: 15424K(20480K)->64K(20480K) Eden: 15360K(19456K)->0K(19456K) From: 64K(1024K)->64K(1024K)
[4.183s][info][gc,heap] GC(9) ParOldGen: 27067K(44032K)->42427K(44032K)
[4.183s][info][gc     ] GC(9) Pause Young (Allocation Failure) 41M->41M(63M) 2.049ms
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
```

This was having much more detail to study; starting from space allocation to each area of heap.

Let's look into `GC(0)` event,

```
- Total: 61.5 MB
    |- PSYoungGen: 18944K (~18.5 MB)
        |-  Eden: 16384K (~16 MB)
        |-  From: 2560K (~2.5 MB)
        |-  To: Empty
    |- ParOldGen: 44032K (~43 MB)
```

JVM maintains two survivor spaces but only one is active (From), the other is empty (To) and used as the next target.


Interestingly, in `GC(3)`, we see full (stop-the-world) GC was performed by JVM and the pause was of `6.985ms`,

```shell
[1.154s][info][gc,heap] GC(3) PSYoungGen: 16193K(18944K)->0K(18944K) Eden: 15569K(16384K)->0K(16384K) From: 624K(2560K)->0K(2560K)
[1.154s][info][gc,heap] GC(3) ParOldGen: 31800K(44032K)->21948K(44032K)
[1.154s][info][gc     ] GC(3) Pause Full (Ergonomics) 46M->21M(61M) 6.985ms
```

There can be multiple reason of full GC but in this case I wanted to figure out, let's see the state of memory.

```shell
- PSYoungGen: 15.81MB(18.50MB)->0MB(18.50MB) 
    |- Eden: 15.20MB(16.00MB)->0MB(16.00MB)
    |- From: 0.61MB(2.50MB)->0MB(2.50MB)
- ParOldGen: 
    |- 31.06MB(43.00MB)->21.44MB(43.00MB)
```
We see the young space has ~2.7 MB space but the old has ~ 12 MB but still full GC took place. It seems JVM thought of not promoting the young generation objects to old for some reason. Internally it checked and found some risk of promotion and decided to go with full GC for a safer side. One reason could be that even if the old generation has 12 MB it was fragmented (non-contiguous) space but I wasn't sure. But ultimately JVM detected some risk in promoting objects and thus decided to go for full GC.


I found this in [documentation](https://docs.oracle.com/en/java/javase/21/gctuning/factors-affecting-garbage-collection-performance.html#GUID-4ADBEDE9-5D52-4FBF-ADB2-431C3EB089C5:~:text=At%20each%20garbage,of%20an%20application.),

> At each garbage collection, the virtual machine chooses a threshold number, which is the number of times an object can be copied before it's old. This threshold is chosen to keep the survivors half full. You can use the log configuration `-Xlog:gc,age` can be used to show this threshold and the ages of objects in the new generation. It's also useful for observing the lifetime distribution of an application.

Which points that the JVM keeps a thresold to decide how many times an object can 'survive' before it can move to old generation. I added `-Xlog:gc,gc+age=debug` JVM option to see what this thresold is; and the output was following,

```shell
[0.013s][info][gc] Using Parallel
[0.185s][debug][gc,age] GC(0) Desired survivor size 2621440 bytes, new threshold 7 (max threshold 15)
[0.185s][info ][gc,heap] GC(0) PSYoungGen: 13845K(18944K)->592K(18944K) Eden: 13845K(16384K)->0K(16384K) From: 0K(2560K)->592K(2560K)
[0.185s][info ][gc,heap] GC(0) ParOldGen: 1055K(44032K)->11303K(44032K)
[0.185s][info ][gc     ] GC(0) Pause Young (Allocation Failure) 14M->11M(61M) 10.276ms
5 MB Allocated
[0.196s][debug][gc,age ] GC(1) Desired survivor size 2621440 bytes, new threshold 7 (max threshold 15)
[0.196s][info ][gc,heap] GC(1) PSYoungGen: 11990K(18944K)->672K(18944K) Eden: 11398K(16384K)->0K(16384K) From: 592K(2560K)->672K(2560K)
[0.196s][info ][gc,heap] GC(1) ParOldGen: 11303K(44032K)->21551K(44032K)
[0.196s][info ][gc     ] GC(1) Pause Young (Allocation Failure) 22M->21M(61M) 6.509ms
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
[1.202s][debug][gc,age ] GC(2) Desired survivor size 2621440 bytes, new threshold 7 (max threshold 15)
[1.202s][info ][gc,heap] GC(2) PSYoungGen: 11980K(18944K)->720K(18944K) Eden: 11308K(16384K)->0K(16384K) From: 672K(2560K)->720K(2560K)
[1.202s][info ][gc,heap] GC(2) ParOldGen: 21551K(44032K)->31800K(44032K)
[1.202s][info ][gc     ] GC(2) Pause Young (Allocation Failure) 32M->31M(61M) 5.737ms
[1.210s][info ][gc,heap] GC(3) PSYoungGen: 16350K(18944K)->16350K(18944K) Eden: 15630K(16384K)->15630K(16384K) From: 720K(2560K)->720K(2560K)
[1.210s][info ][gc,heap] GC(3) ParOldGen: 31800K(44032K)->42048K(44032K)
[1.210s][info ][gc     ] GC(3) Pause Young (Allocation Failure) 47M->57M(61M) 5.689ms
[1.217s][info ][gc,heap] GC(4) PSYoungGen: 16350K(18944K)->0K(18944K) Eden: 15630K(16384K)->0K(16384K) From: 720K(2560K)->0K(2560K)
[1.217s][info ][gc,heap] GC(4) ParOldGen: 42048K(44032K)->16828K(44032K)
[1.217s][info ][gc     ] GC(4) Pause Full (Ergonomics) 57M->16M(61M) 6.369ms
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
[2.222s][debug][gc,age ] GC(5) Desired survivor size 1048576 bytes, new threshold 6 (max threshold 15)
[2.222s][info ][gc,heap] GC(5) PSYoungGen: 16094K(18944K)->64K(18944K) Eden: 16094K(16384K)->0K(16384K) From: 0K(2560K)->64K(2560K)
[2.222s][info ][gc,heap] GC(5) ParOldGen: 16828K(44032K)->16828K(44032K)
[2.222s][info ][gc     ] GC(5) Pause Young (Allocation Failure) 32M->16M(61M) 0.705ms
[2.225s][debug][gc,age ] GC(6) Desired survivor size 1048576 bytes, new threshold 5 (max threshold 15)
[2.225s][info ][gc,heap] GC(6) PSYoungGen: 15424K(18944K)->160K(20480K) Eden: 15360K(16384K)->0K(19456K) From: 64K(2560K)->160K(1024K)
[2.225s][info ][gc,heap] GC(6) ParOldGen: 16828K(44032K)->32188K(44032K)
[2.225s][info ][gc     ] GC(6) Pause Young (Allocation Failure) 31M->31M(63M) 2.277ms
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
[3.232s][info ][gc,heap] GC(7) PSYoungGen: 16134K(20480K)->0K(20480K) Eden: 15974K(19456K)->0K(19456K) From: 160K(1024K)->0K(1024K)
[3.232s][info ][gc,heap] GC(7) ParOldGen: 32188K(44032K)->1467K(44032K)
[3.232s][info ][gc     ] GC(7) Pause Full (Ergonomics) 47M->1M(63M) 4.955ms
[3.234s][debug][gc,age ] GC(8) Desired survivor size 1048576 bytes, new threshold 4 (max threshold 15)
[3.234s][info ][gc,heap] GC(8) PSYoungGen: 15360K(20480K)->0K(20480K) Eden: 15360K(19456K)->0K(19456K) From: 0K(1024K)->0K(1024K)
[3.234s][info ][gc,heap] GC(8) ParOldGen: 1467K(44032K)->16827K(44032K)
[3.234s][info ][gc     ] GC(8) Pause Young (Allocation Failure) 16M->16M(63M) 1.567ms
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
[4.240s][debug][gc,age ] GC(9) Desired survivor size 1048576 bytes, new threshold 3 (max threshold 15)
[4.240s][info ][gc,heap] GC(9) PSYoungGen: 15890K(20480K)->64K(20480K) Eden: 15890K(19456K)->0K(19456K) From: 0K(1024K)->64K(1024K)
[4.240s][info ][gc,heap] GC(9) ParOldGen: 16827K(44032K)->32187K(44032K)
[4.240s][info ][gc     ] GC(9) Pause Young (Allocation Failure) 31M->31M(63M) 2.414ms
[4.250s][info ][gc,heap] GC(10) PSYoungGen: 15661K(20480K)->0K(20480K) Eden: 15597K(19456K)->0K(19456K) From: 64K(1024K)->0K(1024K)
[4.250s][info ][gc,heap] GC(10) ParOldGen: 32187K(44032K)->16717K(44032K)
[4.250s][info ][gc     ] GC(10) Pause Full (Ergonomics) 46M->16M(63M) 8.734ms
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
```

The age log, 

```shell
[0.185s][debug][gc,age] GC(0) Desired survivor size 2621440 bytes, new threshold 7 (max threshold 15)
```

points that the thresold 7 meaning Objects surviving `7 Young GCs` will be promoted to the Old Generation (threshold = 7).

For me ths `GC(2)` was an interesting log,

```shell
[1.202s][info ][gc,heap] GC(2) PSYoungGen: 11980K(18944K)->720K(18944K) Eden: 11308K(16384K)->0K(16384K) From: 672K(2560K)->720K(2560K)
```

Here, 
- PSYoungGen: dropped from ~11MB to 720 KB.
- Eden: cleared completely
- Survivor changed from 672 KB to 720 KB; probably moved in `To` survivor space.

```shell
[1.202s][info ][gc,heap] GC(2) ParOldGen: 21551K(44032K)->31800K(44032K)
```

Here old generation size spiked by `~10 MB` due to promotion of objects from young generation increasing it's size to `~31 MB`. Roughly, `1 MB` of memory delta we see which didn't survive the promotion.

Similar thing happened for `GC(3)`, promotion to old generation; space jumped by another `~10 MB` nearing to it's capacity.

```shell
[1.210s][info ][gc,heap] GC(3) ParOldGen: 31800K(44032K)->42048K(44032K)
```

This was the point where the JVM decided to go for full garbage collection in `GC(4)`.

```shell
[1.217s][info ][gc,heap] GC(4) PSYoungGen: 16350K(18944K)->0K(18944K) Eden: 15630K(16384K)->0K(16384K) From: 720K(2560K)->0K(2560K)
[1.217s][info ][gc,heap] GC(4) ParOldGen: 42048K(44032K)->16828K(44032K)
[1.217s][info ][gc     ] GC(4) Pause Full (Ergonomics) 57M->16M(61M) 6.369ms
```

This implies young generation is fully cleared and old was partially cleared. Probably old was cleared first and the young generation objects `~16 MB` was promoted to old generation and then young generation space was cleared completely.


However, I missed on point here, I spawned threads in parallel GC but main didn't wait for them which may end up with improper mesurements considering the JVM may stop GC tracking bit early. I thought of adding `join()` and some additional sleep after allocation to the program. 

```java
public class TryParallelGC {

    public static void main(String[] args) throws InterruptedException {
        Runnable runnable = () -> {
            for(int i = 0; i < 5; i++) {
                byte[] b = new byte[5 * 1024 * 1024];
                System.out.println("5 MB Allocated");
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    throw new RuntimeException(e);
                }
            }
        };

        Thread[] threads = new Thread[6];
        for(int i = 0; i < threads.length; i++) {
            Thread t = new Thread(runnable);
            t.start();
            threads[i] = t;
        }

        for(Thread t : threads) {
            t.join();
        }
    }
}
```
And the output changed a bit but the change wasn't visible easily.

```shell
[0.011s][info][gc] Using Parallel
[0.187s][info][gc,heap] GC(0) PSYoungGen: 13845K(18944K)->672K(18944K) Eden: 13845K(16384K)->0K(16384K) From: 0K(2560K)->672K(2560K)
[0.187s][info][gc,heap] GC(0) ParOldGen: 1055K(44032K)->11303K(44032K)
[0.187s][info][gc     ] GC(0) Pause Young (Allocation Failure) 14M->11M(61M) 10.931ms
[0.199s][info][gc,heap] GC(1) PSYoungGen: 16851K(18944K)->672K(18944K) Eden: 16179K(16384K)->0K(16384K) From: 672K(2560K)->672K(2560K)
[0.199s][info][gc,heap] GC(1) ParOldGen: 11303K(44032K)->26672K(44032K)
[0.199s][info][gc     ] GC(1) Pause Young (Allocation Failure) 27M->26M(61M) 8.145ms
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
[1.208s][info][gc,heap] GC(2) PSYoungGen: 12615K(18944K)->528K(18944K) Eden: 11943K(16384K)->0K(16384K) From: 672K(2560K)->528K(2560K)
[1.208s][info][gc,heap] GC(2) ParOldGen: 26672K(44032K)->31800K(44032K)
[1.208s][info][gc     ] GC(2) Pause Young (Allocation Failure) 38M->31M(61M) 4.182ms
[1.214s][info][gc,heap] GC(3) PSYoungGen: 16092K(18944K)->0K(18944K) Eden: 15564K(16384K)->0K(16384K) From: 528K(2560K)->0K(2560K)
[1.214s][info][gc,heap] GC(3) ParOldGen: 31800K(44032K)->21948K(44032K)
[1.214s][info][gc     ] GC(3) Pause Full (Ergonomics) 46M->21M(61M) 5.776ms
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
[2.221s][info][gc,heap] GC(4) PSYoungGen: 16214K(18944K)->64K(18944K) Eden: 16214K(16384K)->0K(16384K) From: 0K(2560K)->64K(2560K)
[2.221s][info][gc,heap] GC(4) ParOldGen: 21948K(44032K)->27068K(44032K)
[2.221s][info][gc     ] GC(4) Pause Young (Allocation Failure) 37M->26M(61M) 1.900ms
5 MB Allocated
[2.228s][info][gc,heap] GC(5) PSYoungGen: 15612K(18944K)->96K(20480K) Eden: 15548K(16384K)->0K(17920K) From: 64K(2560K)->96K(2560K)
[2.228s][info][gc,heap] GC(5) ParOldGen: 27068K(44032K)->42428K(44032K)
[2.228s][info][gc     ] GC(5) Pause Young (Allocation Failure) 41M->41M(63M) 5.940ms
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
[3.238s][info][gc,heap] GC(6) PSYoungGen: 16179K(20480K)->0K(18944K) Eden: 16083K(17920K)->0K(17920K) From: 96K(2560K)->0K(1024K)
[3.238s][info][gc,heap] GC(6) ParOldGen: 42428K(44032K)->6588K(44032K)
[3.238s][info][gc     ] GC(6) Pause Full (Ergonomics) 57M->6M(61M) 5.744ms
[3.243s][info][gc,heap] GC(7) PSYoungGen: 15360K(18944K)->0K(20480K) Eden: 15360K(17920K)->0K(19456K) From: 0K(1024K)->0K(1024K)
[3.243s][info][gc,heap] GC(7) ParOldGen: 6588K(44032K)->21948K(44032K)
[3.243s][info][gc     ] GC(7) Pause Young (Allocation Failure) 21M->21M(63M) 2.124ms
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
[4.247s][info][gc,heap] GC(8) PSYoungGen: 15957K(20480K)->64K(20480K) Eden: 15957K(19456K)->0K(19456K) From: 0K(1024K)->64K(1024K)
[4.247s][info][gc,heap] GC(8) ParOldGen: 21948K(44032K)->27068K(44032K)
[4.247s][info][gc     ] GC(8) Pause Young (Allocation Failure) 37M->26M(63M) 1.127ms
[4.250s][info][gc,heap] GC(9) PSYoungGen: 15424K(20480K)->64K(20480K) Eden: 15360K(19456K)->0K(19456K) From: 64K(1024K)->64K(1024K)
[4.250s][info][gc,heap] GC(9) ParOldGen: 27068K(44032K)->42428K(44032K)
[4.250s][info][gc     ] GC(9) Pause Young (Allocation Failure) 41M->41M(63M) 1.981ms
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
```

At first the logs look almost similar but with join Threads finishing in sync reduces parallel survivor contention and GC overhead. Aditionally, `join()`, resulting in better coordination and less concurrent allocation pressure. Also, if you look at pause time overall better performance is seen with `join()`. However, this was a very high level observation and detailed comparison was needed to confidently conclude on both.

Interestingly, if I use serial GC in multi-thread program the output looks like following,

```shell
[0.010s][info][gc] Using Serial
[0.104s][info][gc] GC(0) Pause Young (Allocation Failure) 14M->11M(61M) 7.583ms
5 MB Allocated
[0.118s][info][gc] GC(1) Pause Young (Allocation Failure) 27M->26M(61M) 11.406ms
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
[1.132s][info][gc] GC(2) Pause Young (Allocation Failure) 42M->36M(61M) 9.002ms
5 MB Allocated
[1.133s][info][gc] GC(3) Pause Young (Allocation Failure) 51M->51M(61M) 0.032ms
[1.141s][info][gc] GC(4) Pause Full (Allocation Failure) 51M->26M(61M) 8.349ms
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
[2.148s][info][gc] GC(5) Pause Young (Allocation Failure) 42M->36M(61M) 2.239ms
5 MB Allocated
[2.149s][info][gc] GC(6) Pause Young (Allocation Failure) 51M->51M(61M) 0.043ms
[2.156s][info][gc] GC(7) Pause Full (Allocation Failure) 51M->26M(61M) 7.224ms
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
[3.163s][info][gc] GC(8) Pause Young (Allocation Failure) 42M->41M(61M) 6.419ms
[3.164s][info][gc] GC(9) Pause Young (Allocation Failure) 56M->56M(61M) 0.037ms
[3.171s][info][gc] GC(10) Pause Full (Allocation Failure) 56M->26M(61M) 6.806ms
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
[4.177s][info][gc] GC(11) Pause Young (Allocation Failure) 41M->36M(61M) 2.056ms
[4.177s][info][gc] GC(12) Pause Young (Allocation Failure) 51M->51M(61M) 0.041ms
[4.185s][info][gc] GC(13) Pause Full (Allocation Failure) 51M->26M(61M) 7.219ms
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
```

Just look at the pause time, it increases drastically and shoots upto ~11ms. Moreover, Full GC count increased from two to four almost doubled in case of Serial GC; the reason could be inefficient survivor space handling, slower compaction, lower throughput or allocation rate difference.


## G1 GC Play
To overcome challenges of Serial and Parallel GC. G1 brings following characteristics,
- Better heap and CPU utilisation
- Balanced thoughput with pause time goals
- Concurrent marking, sweeping and reclamation
- Focuses on regions with more garbage

The G1 GC handles large heaps of sizes in GB and suited for server grade applications. 

Comparing with our tried GCs I ran the same parallel GC program with G1 GC and the output was following,

```shell
[0.010s][info][gc] Using G1
[0.146s][info][gc] GC(0) Pause Young (Concurrent Start) (G1 Humongous Allocation) 28M->25M(64M) 2.628ms
[0.146s][info][gc] GC(1) Concurrent Undo Cycle
[0.146s][info][gc] GC(1) Concurrent Undo Cycle 0.224ms
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
[1.149s][info][gc] GC(2) Pause Young (Concurrent Start) (G1 Humongous Allocation) 40M->13M(64M) 2.033ms
[1.150s][info][gc] GC(3) Concurrent Undo Cycle
[1.150s][info][gc] GC(3) Concurrent Undo Cycle 0.750ms
[1.152s][info][gc] GC(4) Pause Young (Concurrent Start) (G1 Humongous Allocation) 25M->25M(64M) 1.253ms
[1.152s][info][gc] GC(5) Concurrent Undo Cycle
[1.153s][info][gc] GC(5) Concurrent Undo Cycle 0.551ms
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
[1.155s][info][gc] GC(6) Pause Young (Concurrent Start) (G1 Humongous Allocation) 39M->25M(64M) 0.891ms
[1.155s][info][gc] GC(7) Concurrent Undo Cycle
[1.155s][info][gc] GC(7) Concurrent Undo Cycle 0.071ms
5 MB Allocated
5 MB Allocated
[2.157s][info][gc] GC(8) Pause Young (Concurrent Start) (G1 Humongous Allocation) 38M->13M(64M) 2.088ms
[2.157s][info][gc] GC(9) Concurrent Undo Cycle
[2.158s][info][gc] GC(9) Concurrent Undo Cycle 0.461ms
5 MB Allocated
[2.160s][info][gc] GC(10) Pause Young (Concurrent Start) (G1 Humongous Allocation) 31M->31M(64M) 1.331ms
[2.160s][info][gc] GC(11) Concurrent Mark Cycle
5 MB Allocated
5 MB Allocated
5 MB Allocated
[2.167s][info][gc] GC(11) Pause Remark 51M->51M(64M) 0.488ms
5 MB Allocated
5 MB Allocated
[2.167s][info][gc] GC(11) Pause Cleanup 52M->52M(64M) 0.049ms
[2.168s][info][gc] GC(11) Concurrent Mark Cycle 8.109ms
[3.171s][info][gc] GC(12) Pause Young (Prepare Mixed) (G1 Humongous Allocation) 58M->19M(64M) 1.146ms
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
[4.175s][info][gc] GC(13) Pause Young (Mixed) (G1 Humongous Allocation) 58M->7M(64M) 1.426ms
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
5 MB Allocated
```

In above logs,

```shell
[0.146s][info][gc] GC(1) Concurrent Undo Cycle
[0.146s][info][gc] GC(1) Concurrent Undo Cycle 0.224ms
```
This event is responsible for _undoing_ speculative work or cleaning up remembered sets metadata that may no longer be needed. First log is initiation log and second one is completion with time taken, 0.224ms.

```shell
[0.146s][info][gc] GC(0) Pause Young (Concurrent Start) (G1 Humongous Allocation) 28M->25M(64M) 2.628ms
```
Here Young GC is triggered due to humongous allocation (>= 50% of region size typically > 1 MB).  This also starts concurrent mark cycle.


```shell
[2.160s][info][gc] GC(11) Concurrent Mark Cycle
...
[2.167s][info][gc] GC(11) Pause Remark 51M->51M(64M) 0.488ms
...
[2.167s][info][gc] GC(11) Pause Cleanup 52M->52M(64M) 0.049ms
[2.168s][info][gc] GC(11) Concurrent Mark Cycle 8.109ms
```

GC begins the marking concurrently in background to identify the live objects in the old generation. Followed by Pause Remark and Pause Cleanup, here Pause means STW (Stop-the-world) events. Both these consist of final marking and metadata clean up; preparing it for Mixed GC to follow in below events logs.

```shell
[3.171s][info][gc] GC(12) Pause Young (Prepare Mixed) (G1 Humongous Allocation) 58M->19M(64M) 1.146ms
...
[4.175s][info][gc] GC(13) Pause Young (Mixed) (G1 Humongous Allocation) 58M->7M(64M) 1.426ms
```

The G1 and Parallel GC finished it faster if the scale is increased of object creation to 10x. However, this was a small experiment to see how each GCs are doing thus can not be a parameter to performance; each GC has their own place and it all depends on usecase.

```
Serial: ~300 Seconds
Paralle: ~50 Seconds
G1: ~50 Seconds
```

There is still lot to try and test with GC and I will be doing it in future as time permits.
