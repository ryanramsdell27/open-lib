# open-lib
Distributed, communal library targeting textbook exchange for the education community.

## Inspiration
Thousands of textbooks are purchased for a semester, used lightly, and left in a corner for years to come. Open Lib aims to reduce unnecessary book production and save college students cash from purchasing.

## What it does
Open Lib is a communal, distributed library. Users can register, post books, and request books with a physical transaction layer that asserts an exchange has occurred between users. Books can be added or removed from the library at a whim and are unavailable while a physical transaction is pending.

## How we built it
Open Lib was built with Flask, MongoDB, and Bootstrap. Sessions are securely stored in Json Web Tokens allowing persistent user interaction.

## Challenges we ran into and learned from
We were both inexperienced in MongoDB and Flask, so there were plenty of things to learn. The biggest challenge came from planning when deciding how detailed we should be before the implementation step. We learned it's better to be articulate with our planning to avoid later confusion during implementation. This meant defining tables, user flows, actions, etc.

## Accomplishments that we're proud of
We're incredibly proud of the end result. We were able to smoothly collaborate and divide work such that there were no major dependencies between our jobs. It is safe to say we ended with an MVP.

## What's next for Open Lib
There is potential to move Open Lib to be completely P2P. Universities would be able to host an entry point for the network that authenticate's with their login services (NetID). After that, the user is free to join and post books. It is a simple modification to current P2P networks such as Chord that distribute <filename, file location> tuples to be <bookname, book owner>.
