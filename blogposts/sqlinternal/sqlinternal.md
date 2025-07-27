---
layout: post
permalink: /
title: How SQL works internally?
post: 7255763826326265029
labels: sql
---

<img src="./images/cover.png" height="420px" width="820px" />

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


<img src="./images/phases.png" height="420px" width="820px" />

A query goes through many phases to finally return the required result.

- **Parsing**: Build a parse tree from a query if it's valid.
- **Binding**: Build a query processor tree using parse tree.
- **Optimization**: Determine effcient execution plan.
- **Execution**: Carry out chosen execution plan.

## Storage Layer
This layer manages how data is physically stored and accessed.

<img src="./images/storage.png" height="320px" width="520px" />

The smallest data unit in storage is called page which is generally of 8KB. When there is a request to fetch the data it first checks in buffer (cache), if the data page is present it uses it otherwise looks into data file.

Two additional mechanisms background job, to clean up dirty pages, and transcation log, for durability and recovery are in place.