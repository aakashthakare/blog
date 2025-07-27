---
layout: post
permalink: /
title: How SQL works internally?
post: 7255763826326265029
labels: sql
---

![](./images/cover.png)

## Introduction
SQL Database engine has primarily two components - Compiler and Virtual Machine.

Compiler is responsible to convert human readable query to machine understandable bytecode, which further understood and executed by the virtual machine.

SQL systems majorly follows a three layer architecture,
- Protocol Layer
- Query Processing Layer
- Storage Layer


## Protocol Layer
This layer is responsible for the communication takes place between the client and the SQL server using network protocol.

Authentication takes place in this layer; when we login to the database using the credentials.

Common errors that we observe in this layer includes following,
- Connection failure
- Hand shake failure
- Authentication errors
- Protocol mismatch etc.

## Query Processing Layer
When we want to learn about internal working of SQL, we first need to understand different phases a query goes through.


![](./images/phases.png)

A query goes through many phases to finally return the required result.

- **Parsing**: Build a parse tree from a query if it's valid.
- **Binding**: Build a query processor tree using parse tree.
- **Optimization**: Determine effcient execution plan.
- **Execution**: Carry out chosen execution plan.

## Storage Layer
This layer manages how data is physically stored and accessed.

![](./images/storage.png)