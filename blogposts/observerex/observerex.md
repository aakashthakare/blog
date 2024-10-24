---
layout: post
permalink: /
title: Observer Pattern
post: 2466173168202911654
labels: Java, Design Pattern
---

Observer pattern is widely used in many real time applications. It is one of the behavioural design patterns. In this post we will try to understand it and try to answer questions around it.

Let's understand it with an example of stock market.

<img src="./imgs/image%20copy.png" height="420px" width="820px" />

Basic idea is to observe something and get notified based on some condition so that observer can take necessary action accordingly.

With following Java program it becomes a bit more cleared on how this design pattern fundamentally works.

```java
class Stock {
    String name;

    double price;

    public Stock(String name, double price) {
        this.name = name;
        this.price = price;
    }
}

class StockMarket {

    private List<Stock> stocks;

    private List<StockObserver> observers;

    StockMarket() {
        observers = new ArrayList<>();

        stocks = new ArrayList<>();
        stocks.add(new Stock("Apple", 1000.23));
        stocks.add(new Stock("Google", 1000.23));
        stocks.add(new Stock("Microsoft", 1000.23));
        stocks.add(new Stock("Facebook", 1000.23));
        stocks.add(new Stock("Tesla", 1000.23));

    }

    public void start() throws InterruptedException {
        Random random = new Random();

        while(true) {
            Thread.sleep(1000);
            Stock stock = stocks.get(random.nextInt(stocks.size()));
            stock.price = random.nextDouble();
            observers.forEach(o -> o.movement(stock));
        }
    }

    public void register(StockObserver observer) {
        this.observers.add(observer);
    }

}

interface StockObserver {

    void movement(Stock stock);

}


class Trader implements StockObserver {

    @Override
    public void movement(Stock stock) {
        System.out.printf("%s stock price %f\n", stock.name, stock.price);
    }
}
```

Note that the `StockMarket` is completely unaware of the underlying observer. Any class can be a observer not necessarily it to be a `Trader`. However, every `Trader` will be a `StockObserver` by default. 

Consider a scenario where a `Trader` is interested in specific stock and not all stock. We can think of two options here,
1. `StockMarket` can register `Trader` for specific `Stock`.
2. `Trader` can act on specific `Stock` and ignore the other movements.

#### Which option is more suitable here and why?
Preferred choice may be first one as it stops flow of unneccessary information to `Observer` which they are not interested in and saves function calls.

#### What if `StockMarket` is overloaded with lot of observers?
Considering the example, there can be lot of `Trader`s observing the stock market and wants a real time information. For each and every stock the pattern used will not likely going to scale. It may work but it may end up with higher latency.

#### What if one of the `Observer` call fails!?
All the subsequent observers should get notifications. Otherwise we may need to perform check to see whether the observer is active or not before notifying. In above example, if any of the observer fails it will not notify remaining observers.

#### Should StockMarket be responsible for notifying observers?
That's a valid question. It can be moved to separate class to filter out events and notify to respective observers.

This is pretty simple implementation of the observer pattern. We may need to look into other aspects of the system to deal with the issues arising in current design. For example, rather than immediately updating we can build a queue to fan out. But that's not the solution in all use cases. We need to take a wholestic view of the business and system requirements into consideration to decide the possible approach.

### Summary
The observer pattern is a behavioural pattern which can be used to notify one or more observers of the subject in case of any state change. It's crutical to understand the scalability, performance concerns and heavy dependency on observer interface before adapting this pattern on a large scale use case.