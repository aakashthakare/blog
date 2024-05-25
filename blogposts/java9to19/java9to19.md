---
layout: post
permalink: /
title: Java 9 to 19
post: 4354712550862386194
---

Java 8 is still extensively used in the industry and many applications will gradually shift to newer Java version, especially the LTS versions. 

In this post we will take a look at the evolution happened in Java language from Java 9 to Java 19. Note that each version comes with many improvements, bug fixes and variety of features, we will cover the ones which are majorly used and can impact our day to day developement.

## Java 9
- Factory methods for collection
```
    List immutableL = List.of(1, 2, 3);
    Map immutableM = Map.of(1, "ONE", 2, "TWO", 3, "THREE")
```
- JShell: Java Shell, or REPL (Read Evaluate Print Loop) to execute java constructs directly in command line.
<img src="images/jshell.png">

- Private methods in interface. This will avoid code duplication and better separation of concern when it comes to implementing default and static methods in interface.
```
    interface Student {
    private String joinNames(String firstName, String lastName) {
        return String.join(firstName, " ",lastName);
    }
    private static String schoolName() {
        return "Some School";
    }

    default String id(String firstName, String lastName) {
        String fullName = joinNames(firstName, lastName);
        return schoolName() + "\n" + fullName;
    }
}
```

- Step in a direction to optimize String concatenation.

For the given class,
```
public class Test {
    public static void main(String[] args) {
        String str = args[0] + " and " + args[1];
    }
}
```

If we compile and check the bytecode, we can notice significant different in the way concatenation is handled. 

In Java 8
```
➜  java git:(main) ✗ java -version 
openjdk version "1.8.0_362"
OpenJDK Runtime Environment (build 1.8.0_362-bre_2023_01_22_03_30-b00)
OpenJDK 64-Bit Server VM (build 25.362-b00, mixed mode)
➜  java git:(main) ✗ clear           
➜  java git:(main) ✗ java -version
openjdk version "1.8.0_362"
OpenJDK Runtime Environment (build 1.8.0_362-bre_2023_01_22_03_30-b00)
OpenJDK 64-Bit Server VM (build 25.362-b00, mixed mode)
➜  java git:(main) ✗ javac Test.java
➜  java git:(main) ✗ javap -c  Test 
Compiled from "Test.java"
public class Test {
  public Test();
    Code:
       0: aload_0
       1: invokespecial #1                  // Method java/lang/Object."<init>":()V
       4: return

  public static void main(java.lang.String[]);
    Code:
       0: new           #2                  // class java/lang/StringBuilder
       3: dup
       4: invokespecial #3                  // Method java/lang/StringBuilder."<init>":()V
       7: aload_0
       8: iconst_0
       9: aaload
      10: invokevirtual #4                  // Method java/lang/StringBuilder.append:(Ljava/lang/String;)Ljava/lang/StringBuilder;
      13: ldc           #5                  // String  and
      15: invokevirtual #4                  // Method java/lang/StringBuilder.append:(Ljava/lang/String;)Ljava/lang/StringBuilder;
      18: aload_0
      19: iconst_1
      20: aaload
      21: invokevirtual #4                  // Method java/lang/StringBuilder.append:(Ljava/lang/String;)Ljava/lang/StringBuilder;
      24: invokevirtual #6                  // Method java/lang/StringBuilder.toString:()Ljava/lang/String;
      27: astore_1
      28: return
}
```

In Java 9,

```
➜  java git:(main) ✗ java -version 
openjdk version "9"
OpenJDK Runtime Environment (build 9+181)
OpenJDK 64-Bit Server VM (build 9+181, mixed mode)
➜  java git:(main) ✗ javac Test.java
➜  java git:(main) ✗ javap -c  Test 
Compiled from "Test.java"
public class Test {
  public Test();
    Code:
       0: aload_0
       1: invokespecial #1                  // Method java/lang/Object."<init>":()V
       4: return

  public static void main(java.lang.String[]);
    Code:
       0: aload_0
       1: iconst_0
       2: aaload
       3: aload_0
       4: iconst_1
       5: aaload
       6: invokedynamic #2,  0              // InvokeDynamic #0:makeConcatWithConstants:(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;
      11: astore_1
      12: return
}
```

Notice the multiple `StringBuilder` invocations in case of Java 8, which is replaced with `makeConcatWithConstants` in Java 9.

## Java 10

## Java 11

## Java 12

## Java 13

## Java 14

## Java 15

## Java 16

## Java 17

## Java 18

## Java 19