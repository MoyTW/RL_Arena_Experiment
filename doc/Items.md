# Items

All items must be wielded before usage. For example, if you wish
to throw a grenade, you must first either drop/stow the weapon or
item you're holding in your hand (probably your dominant hand but
I dunno if I want to go that far), then prime it with your other
hand, and finally throw it. This makes throwing a grenade a
two-hand operation.

Likewise, if you want to try and net something, you'll need to
have at least one hand free to throw the net. Probably two would
be helpful, but I guess it'd be kind of doable with one.

While I don't intend to have potions and scrolls, under this
system, you would also have to have a hand free to drink a potion
or hold a scroll or zap a wand or what have you.

I have no idea if this actually improves roguelike gameplay (I
suspect it'd be really annoying in that context) but it will mean
that adventurer equipment such as easily-reachable pouches and
harnasses for carrying stuff into battle (which would reduce the
time spent swaping out items) will be highly important. This
means preparation will be extremely important. What the person
decides to put in their pouches and what they decide to leave in
their packs might be a life-of-death decision.

Given this "You must have an item in your hand to use it!" how
will we reflect that?

Let's think out loud.

Items could have the following states:

* In-hand and ready for usage (for humans - I guess if you have a
  four-armed tentacle tool-user they'd have it in-tentacle?
  in-claw? eh it's not that important)
* In a easily accessible harnass/pouch/whatever (they could stick
  things to their hats! like jaegers)
* On the ground nearby (did the English do this one? put a bunch
  of arrows on the ground when they formed their formations?)
* In a rucksack/pack/carrying thing

Obviously, once an item is in-hand, there's no need for any
further action to use it. You can swing your sword, shoot your
gun, or throw your grenade. This state could be called 'held' or
something. Once you have an item 'held', transitioning to the
other states would look something like:

Held->Rigged = Fast
Held->Dropped = Instant
Held->Pack = Slow

I guess I just decided to tentatively call 'in your ammo
pouch/quiver/whatever' 'rigged', which gives us:

Rigged->Held = Fast
Rigged->Dropped = Fast (is Rigged->Held->Dropped)
Rigged->Pack = Very Slow (is Rigged->Held->Pack)

Basically, all the transitions go through Held. Seems obvious in
hindsight.

Would 'held' be effectively a subset of 'equipped' or would it be
its own completely different thing? For that matter, is a
'rigged' item considered 'equipped'? I think the answer is 'no' -
the definition of 'equipped' seems closer to 'worn on body' once
we remove the 'held' concept from it. For example, you wear boots
on your body. However, you also wear a sheathed sword on your
body, and calling a sheathed sword equipped would just end up
confusing everybody! So, how about we dump equipped and go with
'worn' or something? You wear your boots, you wear your cloak,
and you wear your armor. When your sword is sheathed, you...wear
the sheathe? You can definitely wear a grenade belt, and I guess
if you think about, who was it? Rambo? he was wearing an ammo
belt, right? And I presume at some point he 'held' the ammo belt
to feed it into a machine gun.

I dunno, I never watched Rambo.

So we have the following states:

* Held: It's in your hand
* Rigged: It's in an easy-to-access container on your body
* Worn: It's on your body, as in, it's an article of clothing
* Stored: It's on you, but it'll take some work to get to it
* Dropped: It's on the ground at your feet

So what would a dagger in your boot be? Would it be rigged? Would
it be worn? Would it be stored? Well, let's see...it depends! Do
you have extensive training in dagger-in-boots and also a boot
sheathe that's easy-to-access? Then it'd be rigged. Are you
trying to smuggle a dagger into the Palace for nefarious
purposes? It'd probably be stored. It's almost definitely never
going to be 'worn' because a dagger's not really an article of
clothing.

Let's say you have a Really Big Sword, like one of them swords
they have in Dark Souls. First off, it's basically impossible for
a Dark Souls sword to be rigged; you would have to carry it
around in a sheathe (the sheathe I guess would be a rigging tool
that you'd wear) but then you'd have to pull it out somehow and
that's not fast at all! I mean, if the sword's as big as you
you'd have to basically detach the mount every time you want to
take out the sword. So that kind of weapon would really only be
able to be Held, Stored, or Dropped. But then surely there's a
difference between having your Great Big Sword in a pack and
having it in a sheathe on your back?

Eh, you know what, don't worry about it too much.

So, riggings! Most weapons have their own riggings. For example,
a sword (weapon) has a sheathe (rigging) which is usable only by
that weapon. You wear the rigging, and you, uh, rig the weapon in
the rigging? Some weapons, however, have no rigging. For example,
a rifle has at most a strap; otherwise, you just have to carry it
at all times.

What does WW1/WW2 soldiers do with their rifles when they threw
grenades, then? Put them on the ground real quick and then grab
them after they threw them? Or did they all have rifle straps?

I have just attempted to look this up on my phone and apparently
the preferred terminology is "sling" as in "rifle sling". Good to
know. Since you wear a rifle sling and a sling is part of the
rifle, this turns the rifle into...its own rigging. Eh. You know,
how about I just split those two apart and have you 'wear' a
rifle strap, which provides a mount point for the rifle? Yeah
that sounds good.

# RESULTS

All items have the following possible states:
* Held: It's in your hand
* Rigged: It's in an easy-to-access container on your body
* Worn: It's on your body, as in, it's an article of clothing
* Stored: It's on you, but it'll take some work to get to it
* Dropped: It's on the ground at your feet

All items must be *held* to use. This includes wearable items -
if you want to put on a belt, you must first pick the belt up out
of the dresser and *hold* it.

In order for an item to be *rigged*, there must be a *mount
point* on the person that is compatible with that specific
item. The *mount point* is attached to a piece of equipment which
then must be *worn*.
