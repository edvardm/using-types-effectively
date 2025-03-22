
# Using Types More Effectively

In this article, we'll explore practical ways to leverage static typing in Python—primarily through the [mypy](https://mypy-lang.org) type checker—from basic union types to more refined concepts like phantom types. To keep things a bit more interesting, we'll apply these ideas to a fantasy-themed dungeon crawler RPG setting, illustrating how thoughtful domain modeling can neatly sidestep entire classes of bugs.

The core idea here is straightforward yet powerful: **_making invalid states unrepresentable_** by just using types. This clever strategy helps us catch numerous errors at compile-time (or, in Python’s case, during type analysis), significantly reducing the likelihood of bugs that might otherwise inconvenience end users.

While this principle shines brightest in compiled languages, excellent work accomplished by mypy developers can bring us most of the same benefits. Rather than just preventing trivial mistakes (like letters sneaking into postal codes), a well-structured type system can express complex, logical transitions without adding any runtime overhead. Done right, this approach doesn't just prevent errors; it also makes code easier to read and maintain.

Additionally, it can reduce or entirely eliminate certain forms of errors. If a condition simply _cannot_ occur according to your types, there's no need to test for it explicitly.

> **Note**: All examples assume Python 3.10+ to leverage the `match` statement and modern `|` syntax for union types.

## 0. Common Pitfalls

Before diving deeper, let's quickly touch on some common unfortunate practises several Python developers often make even when working with critical codebases:

- **Overusing `Any` and vague types**: While liberally sprinkling code with `Any` might silence type-checker warnings, it also defeats the very purpose of having type annotations. Being overly permissive easily leads to subtle bugs lurking undetected.

- **Neglecting strict mode**: Many developers miss out by not enabling stricter settings in their type checker, like mypy's `--strict`. This leniency leaves unnecessary room for error.

- **Misunderstanding runtime versus compile-time checks**: using `isinstance()` might bet better than nothing, but such checks are best left for type system.

The core objective of effective typing isn't just error detection, but clarity and maintainability. Well-designed types can make the code easier to understand, reducing cognitive overhead. However, poorly designed or overly complex annotations can have the opposite effect. If your annotations start obscuring your logic rather than clarifying it, consider simplifying your approach.

## 1. Constrained Values: From Strings to Enums

When modeling fixed sets of options, we have several approaches at our disposal. Let us examine them in order of increasing sophistication, using a single, simple function as an example. Assuming our hero needs to be able to attack various monsters lurking in the darkness, we could come up with something like

```python
!include src/ex_1_simple.py
```

This approach, while functional and common, presents some regrettable limitations:

- No compile-time validation
- Typos in string literals won't be caught until runtime
- No IDE autocompletion support
- Documentation of valid values is not visible in the code (if anywhere)

In particular, the type checker will not warn about `attack_enemy("railgun", "special")` until runtime. One option would be to turn return value into `int | None` and use non-strict dictionary access, but then we would taint all calls and introduce potential None error, forcing callers to (often repeatedly) check for None, or risk throwing `KeyError` with current implementation.

### Improved approach using `Literal`

```python
!include src/ex_1_literal.py
```

Using  `Literal` we define precisely which values are permissible, gaining compile-time validation via type checker. It enables IDE autocompletion, and documents valid values directly within the type system. The code becomes more maintainable, as addition of new values forces updating the type definition.

### Using `Enum`

```python
!include src/ex_1_better.py
```

This final version employing enums offers additional advantages. Values are grouped in more prominent fashion with an explicit namespace. Enum values may be modified without disrupting serialized data. Enums are self-documenting, may easily include docstrings (as values), while still providing full IDE autocompletion.

## 2. Union Types for Basic ADTs

We already saw how enums can be used to constrain allowed values to prevent typos or other coarse errors. In general, what we often want to do though is to create _Algebraic Data Types_ ([ADT](https://en.wikipedia.org/wiki/Algebraic_data_type)s) to model idea of varying options without making code more fragile or convoluted with unnecessary checks.

Let's define some terms first: while unions and sum types are often used interchangeably, they have a crucial difference: a union type may hold any of the specified types simultaneously, while a sum type can hold exactly one of the specified types at a time. In other words, a sum type is a union type with a constraint that only one variant can be held at a time. Sum types are also known as tagged unions, discriminated unions, or algebraic data types (ADTs).

> While Python's `|` syntax creates a **union type**, we are using it here to model a **sum type**, where each variant is a **distinct, disjoint case** of an overarching concept. In some languages (e.g., Haskell, Rust, OCaml, Idris), sum types are first-class language features with explicit syntax. Python lacks direct support, but we can **emulate** sum types with combined use of unions and dataclasses.

Let's examine a more refined implementation:

```python
!include src/ex_2_better.py
```

This implementation offers several advantages over our previous dictionary-based approach. First, the type checker provides static verification, ensuring that `use_item` only accepts our defined classes. The code becomes more readable as each type's properties are explicitly defined in the class structure. When we need to extend our system with new variants (such as adding an `Armor` class), the type checker will immediately alert us if we haven't handled the new case. Perhaps most elegantly, the `match` statement works harmoniously with our sum type, providing a clean and exhaustive way to handle all possible variants without nested conditionals.

The last point is worth emphasizing: `match` plays particularly well with sum types, so unless the condition is trivial, we prefer `match` over `if`. The code is also more clear to read, as each case is necessarily compared against the same, single expression.

> 📚 A **sum type** represents a value that can be of **either** type A **or** B, but not both.
>
> If we let $S = A + B$, then cardinality $|S| = |A + B| = |A| + |B|$

## 3. NewType for Domain-Specific IDs

`NewType` is a powerful feature for distinguishing semantically different values that share the same base type. While similar to `Literal`s in that it constrains values, it works at the type level rather than the value level.

In our dungeon crawler, we might have different types of IDs that are all integers at runtime but represent different concepts in our domain. For example, a character's health points and their level are both integers, but they represent fundamentally different things. Let's see how we can use `NewType` to prevent mixing these up:

```python
!include src/ex_3.py
```

This approach provides more type safety, as the type checker will catch any attempts to mix up different types of IDs with zero runtime overhead, since `NewType` is erased at runtime. It also makes code more self-documenting, as the type system prominently indicates what kind of ID is expected.

## 4. Generics for Type-Safe Collections

Generics let you define reusable data structures that preserve type information. They build upon the concept of union types by allowing us to work with collections of any type while maintaining type safety.

In our dungeon crawler, we might want to create a type-safe inventory system that can hold different types of items while ensuring we can't mix incompatible items. Let's see how generics can help:

```python
!include src/ex_4.py
```

This example demonstrates several key benefits of generics. First, the type system knows exactly what kind of items are in each inventory, preserving type information throughout your code. Second, the type checker ensures we can't mix incompatible items, catching errors at compile time rather than runtime. Third, the same inventory code works with any type of item, making it highly reusable across your codebase. Finally, you get full IDE support with autocompletion for item-specific methods, improving developer productivity and reducing errors.

As a common example, generics allow us to write flexible functions such as `filter`, `fold` (`reduce` in Python) and `map`. These are all _parametrically polymorphic, type-preserving_ functions.

### A Word About Functors

> 📚 In category theory, generics are related to _functors_. A functor $F$ is a structure-preserving mapping between categories, which also maintains composition and identity. For type constructors like `list[T]`, the functor maps
>
> $F : \text{Type} \rightarrow \text{Type}$, $F(A) = \text{list}[A]$
>
> For any function $f: A \rightarrow B$, there exists a _lifted_ function $F(f): F(A) \rightarrow F(B)$ that preserves the structure of the type constructor.

Simply put, in programming a functor `F` is a type constructor (like `List`, `Result`, `Tree`...), _and_ a function `f` which operates on normal (unlifted) values of type `T`, returning new function which works on "lifted" values `F(T)` [^1]. Functors are _incredibly powerful_ constructs when a language has built-in support for those, providing developer

- **Composition without boilerplate** allowing perations on collections without manually writing loops or comprehensions
- **Type-safe transformations** with errors caught at compile time
- **Consistent interfaces**: uniform API to work with (vastly) different container types
- **Code reusability** as functions written for simple types can be automatically "lifted" to work on containers of those types

[^1]: They also need to satify functor laws, of which [Wikipedia has a good article](https://en.wikipedia.org/wiki/Functor_(functional_programming))

While functors would not work well with current type systems available for Python, several compiled languages provide these powerful abstractions either natively (Haskell, OCaml, ReasonML) or through well-integrated libraries (like [Cats](https://typelevel.org/cats/) in Scala or [Arrow](https://arrow-kt.io/) in Kotlin).

## 5. Type Guards for Runtime Validation

When you must handle data of uncertain shape (e.g., a JSON payload), _type guards_ let you refine `Any` or union types using runtime checks.

In our dungeon crawler, we might receive item data from a network API or configuration file. The data structure is known but not guaranteed at compile time. Let's see how type guards can help us safely handle this:

```python
!include src/ex_5.py
```

Type guards provide some important benefits. They validate runtime data by ensuring it matches our expected types. They allow us to **narrow types** by helping the type checker understand the specific type after validation has occurred. They handle external data by safely working with information from APIs, configuration files, and other sources. Finally, they maintain type safety by preserving type information throughout your program.

You'll find type guards particularly valuable in several common scenarios. When working with external APIs or data sources, they help ensure the data conforms to your expectations. When parsing configuration files, they validate the structure before you use it. When handling user input, they provide a safety layer between raw input and your core logic. And when converting between different data formats, they ensure the conversion maintains the expected structure.

> 📚 More formally, type guard is a predicate $P(x)$ such that:
>
> $$P : T \to \mathbb{B}$$
>
> $$x : T \land P(x) \Rightarrow x : S \quad \text{where } S <: T$$

## 6. Eliminating Invalid States

Beyond data shapes, we can also address _logical states_. This builds upon the ideas from [Union Types](#2-union-types-for-basic-adts) and [Type Guards](#5-type-guards-for-runtime-validation) to create a more comprehensive type system that can represent complex state machines.

Let's consider a magical artifact system where artifacts can be in different states: unholy, normal, blessed, or radiant. Each state has specific properties and valid transitions.

### Simple Approach

```python
!include src/ex_6_simple.py
```

This approach uses runtime checks and enums to validate state transitions. While more structured than using raw dictionaries, it still has several limitations:

- State transitions are validated at runtime, meaning errors only surface when the code is executed
- The single `Artifact` class with a state field makes it possible to create invalid combinations (e.g., a blessed artifact with healing power)
- Type information is lost, making it harder for the type checker to catch errors
- The code requires manual state checking and error handling
- State transitions are not enforced by the type system
- Blessing can be cast for blessed objets, needlessly triggering expensive animation

### Improved Approach with Type-Based States

```python
!include src/ex_6_better.py
```

Improved approach offers numerous advantages over the simpler implementation. By leveraging the type system, we ensure that artifact transformations follow strict rules. The overloaded `bless_artifact` function demonstrates how we can use the type system to enforce different behaviors based on input type:

```python
@overload
def bless_artifact(artifact: UnholyArtifact) -> NormalArtifact: ...

@overload
def bless_artifact(artifact: NormalArtifact) -> BlessedArtifact: ...
```

Note that the final method with implementation must have exactly the same same name as `@overload`ed typedefs

Now the type system provides strong guarantees about our artifact system, ensuring that only valid state transitions are possible, eg. by preventing attempts to bless already blessed artifacts. Each artifact state has its own specific properties and behaviors clearly defined by its class structure. Most importantly, invalid combinations of states simply cannot exist in our program; the type system makes it impossible to represent scenarios that don't make logical sense in our domain.

There's one big issue though: types we need to represent all possible states is at worst cartesian product of all the types we've declared. Creating dataclasses for each combination can become quickly unwieldy. One solution for this is in the next chapter.

## 7. Phantom Types for Extra Constraints

_Phantom types_ are most useful when we need generic operations that apply to a family of related types. They extend the concepts from [Generics](#4-generics-for-type-safe-collections) and [NewType](#3-newtype-for-domain-specific-ids) to create more sophisticated type-level constraints.

Let's revisit our artifact system from the previous section. The current implementation suffers from a cartesian product explosion of types - we need separate classes for each combination of properties (unholy/normal/blessed × powerful/not powerful × radiant/not radiant). Phantom types can help us avoid this:

```python
!include src/ex_7.py
```

This approach using phantom types provides significant benefits over the previous implementation. By utilizing single `Artifact` class with type parameters, we avoid the combinatorial explosion of classes that would otherwise be necessary to represent all possible states. The phantom types maintain strong type safety while allowing properties to remain truly independent and composable. We can freely combine different states without creating dedicated classes for each combination! Despite this flexibility, the type system continues to enforce valid state transitions through carefully defined overloaded functions. Perhaps most importantly, phantom types introduce zero runtime overhead since they exist purely at the type-checking level and are erased during compilation, resulting in efficient code execution.

## 8. Generalized Algebraic Data Types (GADTs)

GADTs are a powerful feature in languages that support them, enabling you to define data types with a richer structure compared to traditional ADTs. While Python does not support GADTs, the Haskell example below illustrates the core concept. GADTs allow us to define data types where each constructor explicitly specifies or refines the resulting type.

In the following example, `Spell a` is a _parameterized data type_ with parameter `a` [^2]. Traditional ADTs lack the capability for constructors to yield specialized return types like `Spell Int` or `Spell Bool`. GADTs enable this type-level specialization directly through the constructors themselves. GADTs are to types as pattern matching is to values; they allow branching logic at the **type level** depending on which constructor is chosen, thus enabling type refinement and stronger compile-time guarantees.

```haskell
!include src/gadt_8.hs
```

 [^2]: in Haskell, using generic type parameters such as `a` tends to be more common than concrete types such as `Int`

### GADTs with mypy?

mypy does not support GADTs natively, but you can use a combination of type annotations and runtime checks to achieve similar functionality.

## 9. Venturing Further

There are many more advanced concepts in type systems that we haven't covered here. For example:

- **Dependent Types**: Types that depend on other types
- **Type Inference**: Automatically determining types based on usage
- **Type-Level Programming**: Programming at the level of types rather than values

## 10. Conclusion

Using types effectively can greatly enhance the robustness and maintainability of your code. It enables you to catch errors at compile-time, reducing the likelihood of bugs in production. It also makes code more readable and maintainable.

- **Use enums for constrained values**
- **Use union types with dataclasses for basic adts** union types allow you to model multiple possible types
- **Use newtype for domain-specific types with common concrete type**
- **Use generics for type-safe collections**
- **Use type guards for runtime validation**
- **Eliminate invalid states** by expressing valid state transitions using type system
- **Use phantom types for expressing multiple, independent extra constraints**

## 11. Further Reading

For more information on type systems and their applications, consider the following resources:

- **Books**:
  - "Types and Programming Languages" by Benjamin C. Pierce
  - "Programming Language Pragmatics" by Michael Scott
- **Online Resources**:
  - [Type Systems](https://en.wikipedia.org/wiki/Type_system) on Wikipedia
  - [Type Theory](https://en.wikipedia.org/wiki/Type_theory) on Wikipedia
  - [Type Systems in Programming Languages](https://www.cs.cmu.edu/~rwh/courses/612-f09/lectures/02-types.pdf) by Robert Harper
