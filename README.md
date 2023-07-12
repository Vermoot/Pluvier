# The Pluvier Manifesto

> 🇫🇷 **Pourquoi cette page est en anglais ?**
> 
> Même si le projet est porté sur la langue française, le développement de Pluvier se fait en anglais, puisque la plupart des concepts et principes sur lesquels il est basé sont tirés du développement de théories anglophones.
> 
> La communauté OpenSteno étant jusqu'ici quasi-exclusivement anglophone, les discussions liées au développement de la théorie, à la génération du dictionnaire et l'aide apportée par les personnes expérimentées dans le domaine ne peut se faire qu'en anglais.
> 
> Bien évidemment, les ressources d'apprentissage de la théorie, elles, seront écrites en français.


> 🇬🇧 **Why is this page in English?**
> 
> Although this project is all about the French language, Pluvier’s development is done in English, since the majority of concepts and principles on which it’s based come from the development of anglophone theories.
> 
> Since the OpenSteno community is (for now) almost exclusively anglophone, discussion about the theory’s development, dictionary generation, and the help experienced people might bring can only happen in English.
> 
> Of course, the theory’s learning resources will be written in French.

## What is Pluvier?

Pluvier aims to be the first real-time friendly, conflict-free steno theory for French, using the standard Ireland layout and a programmatically generated dictionary.

If you don't understand everything in this sentence, you can learn all about steno, theories and the OpenSteno community [right here](http://www.openstenoproject.org/plover/). Here's a very quick TL;DR: Steno is the fastest way to write on a computer. A theory is the set of rules which allow you to write in steno.

## Why not Grandjean?

Indeed, steno has existed in French for a long time, and is still used today with the Grandjean system. However, the Grandjean theory was not designed with modern real-time applications in mind, and that means it cannot be used in real time without some extra software magic to disambiguate homonyms. The theory isn't **conflict-free**.

Additionally, the Grandjean system uses a different, specific layout that isn't compatible with hobbyist steno boards like the Uni, EcoSteno, etc.

Pluvier, much like Plover does for English, will allow anyone with a hobbyist machine, or even just a compatible keyboard, to steno in French thanks to the Plover software.

## How does Pluvier work?

Pluvier's dictionary is programmatically generated from a set of rules, applied to a huge database of French words containing phonetic transcription, frequency data, grammatical information, and much more. On top of the generated dictionary, a set of briefs and manually-defined outlines will be added.

### A set of rules: The LaSalle theory and a ton of tweaks

Pluvier is mostly based on an existing theory called *La méthode LaSalle,* developped in the late 80s and still used today in Québec.

LaSalle isn't conflict-free, but it's a really solid basis to start from. It seems to be based on StenEd, like Plover, which means many concepts from the English Plover theory are present and many others can be adapted.

There isn't much about LaSalle to be found, but we *do* have a 2003 book detailing its rules pretty extensively. The book being copyrighted, it won't be redistributed here but the whole translated set of rules is available. Most of these rules will be reused in Pluvier, some will be modified to better fit with Plover, and some will be completely different.

### A huge database: Lexique

[Lexique](http://www.lexique.org/) is a collaborative database containing a huge amount of useful data for more than 140.000 French words.
Among other things, it details for (almost) every entry the following infomation:

- **Phonetic transcription**. This is huge for us, because it allows us to generate an outline based on phonetics without having to infer anything from how the word is written. If you know anything about French, you'll get why this is a huge relief.
- **Frequency information**, from either literature, movies, web pages, Twitter... This potentially allows us to determine which word gets priority if homonyms need to be disambiguated.
- **Syllabification** in different forms. This is a bit more iffy, because syllabification is a difficult problem to handle (though crucial for steno), but there's some great info in the database about how a word might be chopped down and some other data allowing *us* to decide how we might want to chop it up. This will be detailed later.
- **Grammatical information**. With some of Pluvier's rules being based on the grammatical form of a word, it's useful to know that the word is a noun, an adjective... For verbs, Lexique even provides data about tenses and conjugation. That means for the conjugated form of a verb, we can know that it's the first-person singular present tense form of the indicative mood. Yeah, French is fun.

tThese two resources are the backbone of Pluvier's dictionary generation, allowing us to write a "script" (bit of an understatement) applying the rules of the theory to the Lexique database, spitting out a json dictionary to be used with Plover.

## Design objectives

- Provide a French theory and dictionary for everyday use, using the standard Ireland steno layout.
- Conflict-free. We should be able to write every word with a different outline.
- Programmatically generated. Outlines should be generated according to the theory rules, as consistently as possible, and manually defined entries should be as rare as possible outside of briefs.
- Predictability. Knowing the theory, the user should be able to write out every word phonetically, syllable-by-syllable, except for a few mandatory briefs for some of the most common words, just like Plover (these words being the first ones you learn and the most common ones you'll write, they won't be a problem)
- Provide some form of syllable-dropping syllabification, à la Plover, to simplify outlines when wanted
- …

## Syllabification [WIP]

Here be some blab about how syllables will be chopped up in written-out outlines, taking a lot from Aerick's Lapwing syllabification specs, and talking about how that could be achieved with the CVC info from Lexique


