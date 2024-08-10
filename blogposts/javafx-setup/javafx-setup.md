---
layout: post
permalink: /
title: JavaFX Project Setup
post: 2518944094852483638
labels: Java,JavaFX,Jar
---

Outline:
- [X] Summary
    - [X] Build desktop application using JavaFX 
- [X] Softwares used
    - [X] IntelliJ Community Edition
    - [X] Java
    - [X] Maven
    - [X] JavaFX SDK for Mac
    - [ ] Environement (Path and Java_home)
- [X] Hello World (using IntelliJ)
    - [-] Create using Maven archtype
    - [X] Import in IntelliJ
    - [X] Changes required to be done in settings of IntelliJ
    - [ ] Run, screenshot
    - [ ] Dependencies javafx-control, graphics, fxml, base (Which are required when)
    - [ ] Access Resources
        - [ ] frxml and css setup
        - [ ] Load Image from resources 
    - [ ] Run, screenshot
- [ ] Plugin to drag and drop components to build UI (Scene Builder https://www.jetbrains.com/help/idea/opening-fxml-files-in-javafx-scene-builder.html#open-in-scene-builder)
- [ ] Module info file guide
- [ ] Create fat Jar
    - [ ] Maven shade plugin to create executable Jar
- [ ] Template Project for JavaFX 
    - [ ] Create a template project in GitHub
- [ ] Closing 
    - [ ] Fix images size


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
- [JavaFX SDK 22.0.2 (for MacOS)](https://gluonhq.com/products/javafx/)
- [Maven 3.8.3](https://maven.apache.org/download.cgi)
- [IntelliJ Idea](https://www.jetbrains.com/help/idea/installation-guide.html)

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

and following plugin,

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

During build and trying some maven command, I ended up with following error,

```
Error occurred during initialization of boot layer
java.lang.module.FindException: Module com.example.hellojavafx not found
```

some articles were suggesting to validate Java and JavaFX versions but that wasn't the issue. Strangely, deleting `target` directory and running the application worked as it is.