# What's this about, then?

The Actions section effectively covers "What can a person do on a
turn" and then "How do you translate that into game terms?"

There should be, at the beginning of an entity's turn, some way
of listing out "Here are all the things you can do." It might end
up looking something like:

* Move to Squares X, Y, Z
* Throw your sword at somebody
* Drop your sword
* Sheathe your sword
* Grab item A, B, C from your belt pouches
* Use Sword Skills D, E, F
* Use Shield Skills G, H, I
* Use Some Random Skills J, K, L

So immediately I'm thinking we can kind of divide this up into
some categories. See:

* Movement-related (go to X, Y, Z)
* Item-related (all the sword stuff, the belt pouch stuff)
* Item-Skill-Pair-related (use sword, shield skills)
* Always-usable-skill-related (use random skills J, K, L)

Technically, you could make movement a skill, though. For
example, 'running real fast' would be a skill...right? I get the
feeling that might end up extremely silly, but you could very
easily end up defining things kind of as follows:

* A very nimble monster has a fast movement-related skill
* A lumbering monster has a slow movement-related skill
* A rhino has two movement-related skills - 'walk' and 'charge'
* A person can 'walk carefully' to avoid damage or 'run' with
  trip chance or just 'hustle' normally

This obviously ends up complicating the time units significantly,
if you decouple the movement from the 1-square=1-turn thing
that's currently going on. On the other hand, it does mean that
'drop everything and run like hell' is a possible tactic and
that's an interesting decision.

The other possible way to manage those 'different movement skill'
schemes is by having the movement skills simply *modify* the base
movement. For example, a 'sprint' skill could just halve your
movement time unit cost until you take some other action.

I am kind of attracted to the 'make literally everything a skill'
approach though, because that means in order to present the list
of actions all you need to do is run down every skill,
invalidating the ones that are impossible to carry out. Then I
guess you have to join in the inventory management ones, so it's
not all sugar.

Even if you don't go whole hog on the 'movement and basic attacks
are also skills' thing though, you can still wrap everything up
in a PossibleAction class or something to present when you ask
"What can I do?"