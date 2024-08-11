---
layout: post
permalink: /
title: JavaFX Project Setup
post: 2518944094852483638
labels: Java,JavaFX,Jar
---

## Introduction
Using JavaFX platform, we can build applications for desktop, mobile or embessed systems. It has large set of components to design rich user interface.

JavaFX allows,
- designing the user interface interactively using Scene Builder.
- testing the user inteface using TestFX.
- styling the user interface with the help of CSS.

JavaFX historically used to part of Java installation, however, now it is a standalone component which works on top of JDK. 

I faced multiple challenges during setting up the JavaFX with Java 21 to build a simple application recently. I would like to share the setup I ended up with which may help you as well.

We will be going to use following tools,
- [Java 21](https://docs.oracle.com/en/java/javase/21/index.html)
- [Maven 3.8.3](https://maven.apache.org/download.cgi)
- [IntelliJ Idea](https://www.jetbrains.com/help/idea/installation-guide.html)

Here we will going to use Maven which will take care of downloading required modules, however, you can use JavaFX SDK as well.
- [JavaFX SDK 22.0.2 (for MacOS)](https://gluonhq.com/products/javafx/)

## Project Setup

IntelliJ bundles JavaFX plugin in it.

<img src="images/setup/Screenshot 2024-08-09 at 4.46.14 PM.png" height="520px" width="720px" />

Create New Project in IntelliJ.

<img src="images/setup/Screenshot 2024-08-08 at 10.19.21 PM.png" height="520px" width="720px" />

Select JavaFX in side bar. Select Project SDK as Java 21.

<img src="images/setup/Screenshot 2024-08-08 at 10.20.02 PM.png" height="520px" width="720px" />

For now, we do not need any additional dependencies, we will just click on **Finish**.

<img src="images/setup/Screenshot 2024-08-08 at 10.20.47 PM.png" height="520px" width="720px" />

This will take time finish setting up project and indexing.

<img src="images/setup/Screenshot 2024-08-08 at 10.21.27 PM.png" height="520px" width="720px" />

Once it's ready we can simply run the Main class which is `HelloApplication.java` in this case.

<img src="images/setup/Screenshot 2024-08-08 at 10.24.06 PM.png" height="520px" width="720px" />

It should run successfully and show a window with a button "Hello!".

<img src="images/setup/Screenshot 2024-08-08 at 10.26.59 PM.png" height="520px" width="720px" />

As you can see some gibberish text is shown. You may see following logs in Console.

<img src="images/setup/Screenshot 2024-08-08 at 10.25.48 PM.png" height="520px" width="720px" />

This looked like some issue with the fonts. So I had to add following line in  main method of `HelloApplication.java`.

```java
scene.getRoot().setStyle("-fx-font-family: 'serif'");
```

After running it again it appeared like following,

<img src="images/setup/Screenshot 2024-08-08 at 10.27.34 PM.png" height="520px" width="720px" />




## Changes in POM

If you go to `Project Structure > Modules` you will find many OpenFX dependencies are added. 

<img src="images/setup/Screenshot 2024-08-08 at 10.33.02 PM.png" height="520px" width="720px" />


If we look into `pom.xml` file, we can see following dependecies are add for JavaFX.

```xml
...
<dependency>
    <groupId>org.openjfx</groupId>
    <artifactId>javafx-controls</artifactId>
    <version>11.0.2</version>
</dependency>
<dependency>
    <groupId>org.openjfx</groupId>
    <artifactId>javafx-fxml</artifactId>
    <version>11.0.2</version>
</dependency>
...
```

By default the selected version is `11.0.2` which we will going to change to recent version `22`.

```xml
<dependency>
    <groupId>org.openjfx</groupId>
    <artifactId>javafx-controls</artifactId>
    <version>22</version>
</dependency>
<dependency>
    <groupId>org.openjfx</groupId>
    <artifactId>javafx-fxml</artifactId>
    <version>22</version>
</dependency>
```

However, the build started failing with module error.

<img src="images/setup/Screenshot 2024-08-10 at 9.30.52 PM.png" height="520px" width="720px" />

I had no clue what could have went wrong, so I did clean up and try to build again but didn't work.

Surprisingly, when I executed with command line using `mvn` it worked!

```shell
mvn clean compile
mvn javafx:run
```

Strangely, there is no error in `module-info.java`, from command line it worked well but failing when I run it from IntelliJ. I felt this issue is something specific to IntelliJ and not to JavaFX.

I found the similar problem is discussed on the [forum](https://intellij-support.jetbrains.com/hc/en-us/community/posts/4402811503890-JavaFX-application-with-module-info-java-module-not-found).

I was using IntelliJ CE version shown in following image,

<img src="images/setup/Screenshot 2024-08-10 at 10.01.53 PM.png" height="520px" width="720px" />

Moreover, importing the same project to IntelliJ Ultimate Edition worked miraculously without any modifications. 

<img src="images/setup/dr-strange.png" height="520px" width="720px" />

The `javafx-maven-plugin` is already on latest version, thus we are not changing anything here for now.

```xml
...
<plugin>
    <groupId>org.openjfx</groupId>
    <artifactId>javafx-maven-plugin</artifactId>
    <version>0.0.8</version>
    <executions>
        <execution>
            <!-- Default configuration for running with: mvn clean javafx:run -->
            <id>default-cli</id>
            <configuration>
                <mainClass>com.example.hellojavafx/com.example.hellojavafx.HelloApplication</mainClass>
                <launcher>app</launcher>
                <jlinkZipName>app</jlinkZipName>
                <jlinkImageName>app</jlinkImageName>
                <noManPages>true</noManPages>
                <stripDebug>true</stripDebug>
                <noHeaderFiles>true</noHeaderFiles>
            </configuration>
        </execution>
    </executions>
</plugin>
...
```
## Initialisation Error
During build and trying some maven command, I ended up with following error,

```
Error occurred during initialization of boot layer
java.lang.module.FindException: Module com.example.hellojavafx not found
```

some articles were suggesting to validate Java and JavaFX versions but that wasn't the issue. Strangely, deleting `target` directory and running the application worked as it is.

Also, while running through command for the first time you may get following error,

```shell
[ERROR] Failed to execute goal org.apache.maven.plugins:maven-compiler-plugin:3.8.1:compile (default-compile) on project hello-javafx: Fatal error compiling: error: invalid target release: 0 
```

I noticed that in `maven-compiler-plugin` the source and target version was `0` which I changed to `21` to fix this issue.

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-compiler-plugin</artifactId>
    <version>3.8.1</version>
    <configuration>
        <source>0</source>
        <target>0</target>
    </configuration>
</plugin>
```


## Module Info
Apart from `pom.xml`, you will find one `module-info.java` shown below. Here we can see module dependency on `javafx.controls` and `javafx.fxml` is mentioned. Also, `javafx.fxml` needs to access controllers we will define in out package thus we are opening it.

```java
module com.example.hellojavafx {
    requires javafx.controls;
    requires javafx.fxml;


    opens com.example.hellojavafx to javafx.fxml;
    exports com.example.hellojavafx;
}
```

Whenever you introduce new dependency which you want to be available in your package or you want to open your package to external dependency. Make sure to declare it in `module-info.java` file.


## Executable JAR

To make a runnable `.jar` I used `maven-shade-plugin`.

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-shade-plugin</artifactId>
    <version>2.3</version>
    <executions>
        <execution>
            <phase>package</phase>
            <goals>
                <goal>shade</goal>
            </goals>
            <configuration>
                <transformers>
                    <transformer implementation="org.apache.maven.plugins.shade.resource.ManifestResourceTransformer">
                        <mainClass>com.example.hellojavafx.HelloApplication</mainClass>
                    </transformer>
                </transformers>
            </configuration>
        </execution>
    </executions>
</plugin>
```

I simple ran `mvn clean package` to create the jar file. However when I ran the jar with following command.

```
java -jar target/hello-javafx-1.0-SNAPSHOT.jar
```

It gave me following error,

```
Error: JavaFX runtime components are missing, and are required to run this application
```

To solve this, I had to declare an entry point class which can point to my Application class.

```java
package com.example.hellojavafx;

public class EntryPoint {

    public static void main(String[] args) {
        HelloApplication.main(args);
    }
}
```

This new class I had to use in plugin instead of `HelloApplication`.

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-shade-plugin</artifactId>
    <version>2.3</version>
    <executions>
        <execution>
            <phase>package</phase>
            <goals>
                <goal>shade</goal>
            </goals>
            <configuration>
                <transformers>
                    <transformer implementation="org.apache.maven.plugins.shade.resource.ManifestResourceTransformer">
                        <mainClass>com.example.hellojavafx.EntryPoint</mainClass>
                    </transformer>
                </transformers>
            </configuration>
        </execution>
    </executions>
</plugin>
```

And this time it worked! (*with warning*)

```
➜  hello-javafx java -jar target/hello-javafx-1.0-SNAPSHOT.jar
Aug 10, 2024 10:35:43 PM com.sun.javafx.application.PlatformImpl startup
WARNING: Unsupported JavaFX configuration: classes were loaded from 'unnamed module @673ba40c'
```

The shade plugin adds everything to the classpath and since JavaFX relies on modules this setup breaks the execution. Thus, as a workaround we introduce another class which can be an entry point to the execution instead of JavaFX starter application.