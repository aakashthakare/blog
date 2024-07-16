---
layout: post
permalink: /
title: Some useful stream operations
post: 2298638202796766284
labels:
---
#### Separate Odd and Even numbers  (`List<Integer>` to `Map<String, List<Integer>>`)

```java
Map<String, List<Integer>> oddEvenMap = numbers.stream()  
        .collect(Collectors.groupingBy(i -> (i % 2 != 0 ? "Odd" : "Even")));
```

#### Find distinct values from `Map<String, List<Integer>`

```java
Set<Integer> set = map.values().stream()
					.flatMap(Collection::stream)
					.collect(Collectors.toSet());
```

#### Biggest Odd and Even from List (`List<Integer>` to `Map<String, Integer>`)

```java
Map<String, Integer> bigOddEven = numbers.stream()
											.collect(Collectors.toMap(i -> (i % 2 == 0 ? "Even" : "Odd"),  Function.identity(), (i1 , i2) -> i1 > i2 ? i1 : i2));
```

#### Use value as key and create new map from existing

```java
Map<String, Integer> map = new HashMap<>();  
map.put("a", 1);  
map.put("b", 1);  
map.put("c", 2);  
  
Map<Integer, List<String>> ans = map.keySet().stream().collect(Collectors.groupingBy(map::get));  
System.out.println(ans);
```

Output
```shell
{1=[a, b], 2=[c]}
```

#### Find frequency of each number in list

```java
List<Integer> numbers = new ArrayList<>();  
numbers.add(1);  
numbers.add(2);  
numbers.add(3);  
numbers.add(4);  
numbers.add(4);  
  
Map<Integer, Long> ans = numbers.stream()  
        .collect(Collectors.groupingBy(Function.identity(), Collectors.counting()));  
System.out.println(ans);
```

Output
```shell
{1=1, 2=1, 3=1, 4=2}
```

#### Remove from map based on condition on values

```java
Map<String, Integer> map = new HashMap<>();  
map.put("a", 1);  
map.put("b", 1);  
map.put("c", 2);  
  
map.values().removeIf(i -> i == 1);  
System.out.println(map);
```

Output
```shell
{c=2}
```

#### Distinct and Sum of numbers
```java
Stream<Integer> distinct = numbers.stream().distinct();
int s = numbers.stream().mapToInt(Integer::intValue).sum();
```

#### `IntSummaryStatistics` for Average, Sum, Min/Max
```java
IntSummaryStatistics intSummaryStatistics = numbers.stream().mapToInt(Integer::intValue).summaryStatistics();
double average = intSummaryStatistics.getAverage();
long sum = intSummaryStatistics.getSum();
int max = intSummaryStatistics.getMax();
int min = intSummaryStatistics.getMin();
long count = intSummaryStatistics.getCount();
```