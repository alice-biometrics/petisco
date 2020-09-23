# EventBus :trolleybus:

<img src="https://github.com/alice-biometrics/custom-emojis/blob/master/images/alice_header.png" width=auto>

## Getting Started

Let's image we are working for an organization (e.g `alice`) and developing a new service (e.g `petisco`). 

We want to publish an event when the user is created (`UserCreated`). 
This event will be consumed by:
 * **subscribers**: derived actions that are executed from associated events. 
 
In our example, we are going to use two subscribers:

* `event_store`: general subscriber. It can be useful for saving all events on Elastic, Prometheus, etc...
* `send_mail_handler`: It will send a mail on `UserCreated` event.

The following figure represents this use case:

![Event Bus Example](event-bus-example.jpeg)

What is happening here?

1. The `EventBus` publishes the `UserCreated` domain event. 
  * The routing key of this event is `alice.petisco.1.event.user.created` 
2. The exchange `alice.petisco` (*<organization>.<service>*) redirect the message using the binding keys (*green*)
3. The `store` queue receives the event perfectly :metal:
4. The `alice.petisco.1.event.user.created.send_mail_handler` queue gets the `UserCreated` event.
5. The `send_mail_handler` consumer obtains the event perform the action:
   * If it is success: perfect, everything works nice and the queue will get an `ack` :thumbsup:
   * Otherwise, if it is a failure: something is not working as expected or maybe we are suffering from overload. :fire:
      * We need to recover from error, let's `ack` to `alice.petisco.1.event.user.created.send_mail_handler` and requeue the info to the retry exchange (`retry.alice.petisco`).
      * We select a number of maximun retries, as well as the time between retries (`x-message-ttl` on `retry.alice.petisco.1.event.user.created.send_mail_handler`queue)
6. When the *TTL* expires on the retry queue, the message will be requeues automatically with the following parameters:
  * x-dead-letter-exchange: `alice.petisco`
  * x-dead-letter-routing-key`: `alice.petisco.1.event.user.created.send_mail_handler`
7. Then, the process will return to 2, however in this case, only will be requed to `alice.petisco.1.event.user.created.send_mail_handler` thanks to the additional binding key `retry.alice.petisco.1.event.user.created.send_mail_handler`.

## Naming

The queues naming uses the following convention:

`<organization>.<service>.<version>.<type>.<event_name>.<action_handler>`
  
where:
* **organization** is used for represent your company/team/project
* **service** is used for represent your service/application
* **version** is used for represent the version of the source event/command
* **type** is used for represent the type of source that triggers the process (event|command)
* **event_name** is used to represent the name of the event in snake case (`UserCreate` -> `user.created`) 
* **action_handler** is used to represent the name of the callback which will trigger the event (e.g `send_mail_handler`) 
