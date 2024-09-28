---
layout: post
permalink: /
title: Platform vs. Virtual Threads
post: 5625999940656061571
labels: Java, Thread
---

![](imgs/img.png)


This blog post is a raw comparison of platform and virtual threads. We will use both the types of threads and see how they behave and perform. 

It is important to note that the execution time and other matrics may vary system to system, however, it can definitely give a rough idea about the overall picture. We will try to keep this comparison as fair as possible, if I fail to do so, feel free to post comment below. 

**My System**
- MacBook Pro 
    - RAM 16 GB
    - Processor 2.6 GHz 6-Core Intel Core i7
- Java 21


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
```

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

I thought of replacing `System.out.println(Thread.currentThread().getThreadGroup().getName());` with `System.out.print(".");System.out.print(".");` to keep it simpler.

If we run both methods together from the `main` method,

```java
public class Test {

    public static void main(String[] args) throws InterruptedException {
        platform();
        virtual();
    }

    private static void virtual() throws InterruptedException {
        Thread.startVirtualThread(() -> {
            long start = System.currentTimeMillis();
            for(int i = 0; i < 1000; i++) {
                System.out.println(".");
            }
            long end = System.currentTimeMillis();
            System.out.println("Virtual : " + (end - start) + " ms");
        }).join();
    }

    private static void platform() throws InterruptedException {
        Thread t = new Thread(() -> {
            long start = System.currentTimeMillis();
            for(int i = 0; i < 1000; i++) {
                System.out.println(".");
            }
            long end = System.currentTimeMillis();
            System.out.println("Platform : " + (end - start) + " ms");
        });
        t.start();
        t.join();
    }
}
```

Multiple executions,
- Platform : 19 ms and Virtual : 15 ms
- Platform : 21 ms and Virtual : 24 ms
- Platform : 21 ms and Virtual : 16 ms
- Platform : 22 ms and Virtual : 14 ms
- Platform : 22 ms and Virtual : 29 ms

After changing the sequence of methods the result changes dramatically,

```java
...
public static void main(String[] args) throws InterruptedException {
    virtual();
    platform();
}
...
```

Multiple executions,
- Platform : 17 ms and Virtual : 60 ms
- Platform : 7 ms and Virtual : 35 ms
- Platform : 10 ms and Virtual : 47 ms
- Platform : 9 ms and Virtual : 35 ms
- Platform : 6 ms and Virtual : 30 ms

Okay, lot of confusion here. Let's find answers of each one by one.

### Reason

**Why virtual thread couldn't execute?**

In first case the problem is that the main thread exits before the virtual thread completes it's execution. We can definitely join the virtual thread to our main thread which we did. Again the non blocking behaviour made it behave this way.

```java
public static void main(String[] args) throws InterruptedException {
    virtual();
    Thread.sleep(50000);
}
```

This gives **Virtual : 33 ms**

**Why platform thread executed faster with join?**

In case of virtual threads JVM has to deal with additional work underneath, which leads to slight delay in the execution. Even though it's one thread and we are joining it to main, compared to platform thread it took more time to finish. This ovehead may include things like park/unpark the task based on JVM or CPU bound decision making.


**How sequence of method is impacting the thread task execution time?**

Again the blocking nature of platform thread makes life of virtual thread easier. For platform thread executed first the JVM, CPU or I/O is managed differently compared to virtual thread if executed first. Since the task is pretty simple the impact is significantly lower but such differences can make developer wonder if not understood properly.