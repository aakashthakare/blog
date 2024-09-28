---
layout: post
permalink: /
title: Platform vs. Virtual Threads
post: 5625999940656061571
labels: Java, Thread
---

This blog post is a raw comparison of platform and virtual threads. We will use both the types of threads and see how they behave and perform. 

It is important to note that the execution time and other matrics may vary system to system, however, it can definitely give a rough idea about the overall picture. We will try to keep this comparison as fair as possible, if I fail to do so, feel free to post comment below. 

**My System**
- MacBook Pro 
    - RAM 16 GB
    - Processor 2.6 GHz 6-Core Intel Core i7
- Java 11


## Time to start

**Platform Threads : 21 ms**

```java
private static void platform() {
    long start = System.currentTimeMillis();
    for(int i = 0; i < 100; i++) {
        Thread t = new Thread(() -> System.out.println(Thread.currentThread().getThreadGroup().getName()));
        t.start();
    }
    long end = System.currentTimeMillis();
    System.out.println("Platform : " + (end - start) + " ms");
}
```

**Virtual Threads : 18 ms**

```java
private static void virtual() {
    long start = System.currentTimeMillis();
    for(int i = 0; i < 100; i++) {
        Thread.startVirtualThread(() -> System.out.println(Thread.currentThread().getThreadGroup().getName()));
    }
    long end = System.currentTimeMillis();
    System.out.println("Virtual : " + (end - start) + " ms");
}
```

For 100 Threads the difference doesn't look significant. However, If I increase the count of threads from 100 to 100 the difference increases drastically.

- **Platform Threads : 235 ms**
- **Virtual Threads : 29 ms**

### Reason
Even though the time taken to initialize threads are different, underlying operation would have taken same amount of time. Virtual threads enables better utilisation of  the resources compared platform threads (_virtual thread actually uses platform threads internally_).

The major difference here is that the platform thread managed by OS are blocking, but virtual thread which are managed by JVM are non-blocking. So, in case of virtual thread it will wait for the platform thread to be available but won't block the execution of the program.

## Speed

**Platform : 24 ms**

```java
private static void platform() {
    Thread t = new Thread(() -> {
        long start = System.currentTimeMillis();
        for(int i = 0; i < 1000; i++) {
            System.out.println(Thread.currentThread().getThreadGroup().getName());
        }
        long end = System.currentTimeMillis();
        System.out.println("Platform : " + (end - start) + " ms");
    });
    t.start();
}
```

In case of virtual thread, there is no output in console. Looks like it didn't print anything to console, the thread didn't start.

```java
private static void virtual() {
    Thread.startVirtualThread(() -> {
        long start = System.currentTimeMillis();
        for(int i = 0; i < 1000; i++) {
            System.out.println(Thread.currentThread().getThreadGroup().getName());
        }
        long end = System.currentTimeMillis();
        System.out.println("Virtual : " + (end - start) + " ms");
    });
}

It seems we need to use `join` here.

```java
private static void virtual() throws InterruptedException {
    Thread.startVirtualThread(() -> {
        long start = System.currentTimeMillis();
        for(int i = 0; i < 1000; i++) {
            System.out.println(Thread.currentThread().getThreadGroup().getName());
        }
        long end = System.currentTimeMillis();
        System.out.println("Virtual : " + (end - start) + " ms");
    }).join();
}
```



And it worked, but took comparatively more time than platform thread, almost double.

**Virtual : 49 ms**

Let's try to be fair here,

```java
private static void platform() throws InterruptedException {
    Thread t = new Thread(() -> {
        long start = System.currentTimeMillis();
        for(int i = 0; i < 1000; i++) {
            System.out.println(Thread.currentThread().getThreadGroup().getName());
        }
        long end = System.currentTimeMillis();
        System.out.println("Platform : " + (end - start) + " ms");
    });
    t.start();
    t.join();
}
```

**Platform : 26 ms**

For some reason, platform thread is winning here.