# How to Add a New Message Topic
- In the `models` package, create a Record model that implements the `IRecord` interface. Remember
to update the package index and to create tests.
- In the `MessageParser` class, update the `mapping` class attribute. The key is the topic, which
is usually the first value of the pipe-separated message. The value is the model. Remember to
update the module import statements.
