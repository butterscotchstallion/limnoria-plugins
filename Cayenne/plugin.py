# -*- coding: utf-8 -*-
"""
Cayenne - Displays cat facts or cat gifs based on probability

Copyright (c) 2015, PrgmrBill
All rights reserved.
"""
import supybot.utils as utils
from supybot.commands import *
import supybot.ircmsgs as ircmsgs
import supybot.callbacks as callbacks
import random
import datetime

try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('Cayenne')
except ImportError:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x: x

class Cayenne(callbacks.Plugin):
    """Displays cat facts or cat gifs based on probability"""
    threaded = True
    last_message_timestamp = False
    
    def get_fact(self):
        """
        Get a random cat fact
        """
        facts = ("Cats often overract to unexpected stimuli because of their extremely sensitive nervous system.",
        "You check your cats pulse on the inside of the back thigh, where the leg joins to the body. Normal for cats: 110-170 beats per minute.",
        "When a cats rubs up against you, the cat is marking you with it's scent claiming ownership.",
        "An adult cat has 30 teeth, 16 on the top and 14 on the bottom.",
        "Declawing a cat is the same as cutting a human's fingers off at the knuckle. There are several alternatives to a complete declawing, including trimming or a less radical (though more involved) surgery to remove the claws. Preferably, try to train your cat to use a scratching post.",
        "Cats are subject to gum disease and to dental caries. They should have their teeth cleaned by the vet or the cat dentist once a year.",
        "A domestic cat can sprint at about 31 miles per hour.",
        "The chlorine in fresh tap water irritates sensitive parts of the cat's nose. Let tap water sit for 24 hours before giving it to a cat.",
        "In an average year, cat owners in the United States spend over $2 billion on cat food.",
        "Blue-eyed, white cats are often prone to deafness.",
        "A cat's hearing is much more sensitive than humans and dogs.",
        "Like birds, cats have a homing ability that uses its biological clock, the angle of the sun, and the Earth's magnetic field. A cat taken far from its home can return to it. But if a cat's owners move far from its home, the cat can't find them.",
        "As child Nikola Tesla was inspired to understand the secrets of electricity after being shocked by static electricity from his beloved cat, Macak.",
        "The cat's front paw has 5 toes, but the back paws have 4. Some cats are born with as many as 7 front toes and extra back toes (polydactl).",
        "Spaying a female before her first or second heat will greatly reduce the threat of mammary cancer and uterine disease. A cat does not need to have at least 1 litter to be healthy, nor will they \"miss\" motherhood. A tabby named \"Dusty\" gave birth to 420 documented kittens in her lifetime, while \"Kitty\" gave birth to 2 kittens at the age of 30, having given birth to a documented 218 kittens in her lifetime.",
        "The Maine Coon is 4 to 5 times larger than the Singapura, the smallest breed of cat.",
        "A cat's jaw has only up and down motion; it does not have any lateral, side to side motion, like dogs and humans.",
        "The cat's footpads absorb the shocks of the landing when the cat jumps.",
        "Cats, especially older cats, do get cancer. Many times this disease can be treated successfully.",
        "Cats see six times better in the dark and at night than humans.",
        "Purring not always means happiness. Purring could mean a cat is in terrible pain such as during childbirth. Kitten will purr to their mother to let her know they are getting enough milk while nursing. Purring is a process of inhaling and exhaling, usually performed while the mouth is closed. But don't worry, if your cat is purring while your gently petting her and holding her close to you - that is a happy cat!",
        "On February 28, 1 980 a female cat climbed 70 feet up the sheer pebble-dash outside wall of a block of flats in Bradford, Yorkshire and took refuge in the roof space. She had been frightened by a dog.",
        "In 1987 cats overtook dogs as the number one pet in America.",
        "In 1987 cats overtook dogs as the number one pet in America.",
        "A steady diet of dog food may cause blindness in your cat - it lacks taurine.",
        "A cat uses its whiskers for measuring distances.  The whiskers of a cat are capable of registering very small changes in air pressure.",
        "The Pilgrims were the first to introduce cats to North America.",
        "Cats can get tapeworms from eating fleas. These worms live inside the cat forever, or until they are removed with medication. They reproduce by shedding a link from the end of their long bodies. This link crawls out the cat's anus, and sheds hundreds of eggs. These eggs are injested by flea larvae, and the cycles continues. Humans may get these tapeworms too, but only if they eat infected fleas. Cats with tapeworms should be dewormed by a veterinarian.",
        "Neutering a male cat will, in almost all cases, stop him from spraying (territorial marking), fighting with other males (at least over females), as well as lengthen his life and improve its quality.",
        "A tortoiseshell is black with red or orange markings and a calico is white with patches of red, orange and black.",
        "Kittens lose their baby teeth!! At three to four months the incisors erupt. Then at four to six months, they lose their canines, premolars and molars. By the time they are seven months old, their adult teeth are fully developed. This is one of the ways a vet (or you) can tell the age of a kitten.",
        "The silks created by weavers in Baghdad were inspired by the beautiful and varied colors and markings of cat coats. These fabrics were called \"tabby\" by European traders.",
        "There are approximately 60,000 hairs per square inch on the back of a cat and about 120,000 per square inch on its underside.",
        "Cheetahs do not roar, as the other big cats do. Instead, they purr.",
        "The name \"jaguar\" comes from a Native American word meaning \"he who kills with one leap\".",
        "Cat litter was \"invented\" in 1947 when Edward Lowe asked his neighbor to try a dried, granulated clay used to sop up grease spills in factories. (In 1990, Mr. Lowe sold his business for $200 million.)",
        "A cat has approximately 60 to 80 million olfactory cells (a human has between 5 and 20 million).",
        "The average cat sleeps between 12-14 hours a day.",
        "About 37% of American homes today have at least 1 cat.",
        "Cats have 30 vertebrae--5 more than humans have.",
        "In households in the UK and USA, there are more cats kept as pets than dogs. At least 35% of households with cats have 2 or more cats.",
        "Studies now show that the allergen in cats is related to their scent glands. Cats have scent glands on their faces and at the base of their tails. Entire male cats generate the most scent. If this secretion from the scent glands is the allergen, allergic people should tolerate spayed female cats the best.",
        "Stroking a cat can help to relieve stress, and the feel of a purring cat on your lap conveys a strong sense of security and comfort.",
        "Blue-eyed, pure white cats are frequently deaf.",
        "The smallest breed of domestic cat is the Singapura or \"Drain Cat\" of Singapore. Adult females weigh in at an average of 4lbs.",
        "Tigers have been hunted for their skin, bones, and other body parts, used in traditional Chinese medicine.",
        "Tigers are excellent swimmers and do not avoid water.",
        "Some common houseplants poisonous to cats include: English Ivy, iris, mistletoe, philodendron, and yew.",
        "A cat's normal pulse is 140-240 beats per minute, with an average of 195.",
        "Many cats love having their forehead gently stroked.",
        "The first breeding pair of Siamese cats arrived in England in 1884.",
        "Abraham Lincoln loved cats. He had four of them while he lived in the White House.",
        "A cat's brain is more similar to a man's brain than that of a dog.",
        "Long, muscular hind legs enable snow leopards to leap seven times their own body length in a single bound.",
        "A cat can spend five or more hours a day grooming himself.",
        "Many cats cannot properly digest cow's milk. Milk and milk products give them diarrhea.",
        "Cats purr at the same frequency as an idling diesel engine, about 26 cycles per second.",
        "The cat has 500 skeletal muscles (humans have 650).",
        "The female cat reaches sexual maturity at around 6 to 10 months and the male cat between 9 and 12 months.",
        "Domestic cats purr both when inhaling and when exhaling.",
        "Many people fear catching a protozoan disease, Toxoplasmosis, from cats. This disease can cause illness in the human, but more seriously, can cause birth defects in the unborn. Toxoplasmosis is a common disease, sometimes spread through the feces of cats. It is caused most often from eating raw or rare beef. Pregnant women and people with a depressed immune system should not touch the cat litter box. Other than that, there is no reason that these people have to avoid cats.",
        "Ancient Egyptian family members shaved their eyebrows in mourning when the family cat died.",
        "The life expectancy of cats has nearly doubled over the last fifty years.",
        "Cats' eyes shine in the dark because of the tapetum, a reflective layer in the eye, which acts like a mirror.",
        "Baking chocolate is the most dangerous chocolate to your cat.",
        "Cats walk on their toes.",
        "Cats come back to full alertness from the sleep state faster than any other creature.",
        "A cat will tremble or shiver when it is extreme pain.",
        "On average, a cat will sleep for 16 hours a day.",
        "A cat's field of vision is about 200 degrees.",
        "There is a species of cat smaller than the average housecat. It is native to Africa and it is the Black-footed cat (Felis nigripes). Its top weight is 5.5 pounds.",
        "The average lifespan of an outdoor-only (feral and non-feral) is about 3 years; an indoor-only cat can live 16 years and longer. Some cats have been documented to have a longevity of 34 years.",
        "Every time you masturbate God kills a kitten. Please, think of the kittens.",
        "Has your cat ever brought its prey to your door? Cats do that because they regard their owners as their \"kittens.\" The cats are teaching their \"kittens\" how to hunt by bringing them food. Most people aren't too delighted when a pet brings in their kill. Instead of punishing your cat, praise it for its efforts, accept the prey, and then secretly throw it away.",
        "Cats have 30 vertebrae (humans have 33 vertebrae during early development; 26 after the sacral and coccygeal regions fuse)",
        "Cats have 32 muscles that control the outer ear (compared to human's 6 muscles each). A cat can rotate its ears independently 180 degrees, and can turn in the direction of sound 10 times faster than those of the best watchdog.",
        "Jaguars are the only big cats that don't roar.",
        "A cat has more bones than a human being; humans have 206 and the cat has 230 bones.",
        "A happy cat holds her tail high and steady.",
        "When a cat drinks, its tongue - which has tiny barbs on it - scoops the liquid up backwards.",
        "It may take as long as 2 weeks for a kitten to be able to hear well.  Their eyes usually open between 7 and 10 days, but sometimes it happens in as little as 2 days.",
        "Not every cat gets \"high\" from catnip. If the cat doesn't have a specific gene, it won't react (about 20% do not have the gene). Catnip is non-addictive.",
        "Purring does not always indicate that a cat is happy and healthy - some cats will purr loudly when they are terrified or in pain.",
        "A domestic cat can run at speeds of 30 mph.",
        "Cats lap liquid from the underside of their tongue, not from the top.",
        "A cat will tremble or shiver when it is in extreme pain.",
        "Cats' hearing stops at 65 khz (kilohertz); humans' hearing stops at 20 khz.",
        "The average litter of kittens is between 2 - 6 kittens.",
        "Cats have 30 teeth (12 incisors, 10 premolars, 4 canines, and 4 molars), while dogs have 42. Kittens have baby teeth, which are replaced by permanent teeth around the age of 7 months.",
        "The strongest climber among the big cats, a leopard can carry prey twice its weight up a tree.",
        "Tylenol and chocolate are both poisionous to cats.",
        "On September 6,1950, a four-month-old kitten belonging to Josephine Aufdenblatten of Geneva, Switzerland followed a group of climbers to the top of the 14,691 -ft. Matterhorn in the Alps.",
        "Not every cat gets \"high\" from catnip. Whether or not a cat responds to it depends upon a recessive gene: no gene, no joy.",
        "Normal body temperature for a cat is 102 degrees F.",
        "Cats respond better to women than to men, probably due to the fact that women's voices have a higher pitch.",
        "An estimated 50% of today's cat owners never take their cats to a veterinarian for health care. Too, because cats tend to keep their problems to themselves, many owners think their cat is perfectly healthy when actually they may be suffering from a life-threatening disease. Therefore, cats, on an average, are much sicker than dogs by the time they are brought to your veterinarian for treatment.",
        "Cats can be prone to fleas in the summertime: 794 fleas were counted on one cat by a Cats Protection volunteer in the summer of 1 992.",
        "A female cat will be pregnant for approximately 9 weeks - between 62 and 65 days from conception to delivery.",
        "A tiger's stripes are like fingerprintsâno two animals have the same pattern.",
        "A female Amur leopard gives birth to one to four cubs in each litter.")
        
        return random.choice(facts)
    
    def message_contains_trigger_word(self, message):
        """
        Check prefined list of trigger words and return
        which one was found, if any
        """
        word_string = self.registryValue('triggerWords')
        
        if word_string:
            words = [word.strip() for word in word_string]
            
            if words:
                for word in words:
                    if word in message:
                        return word
            else:
                self.log.error("Cayenne: no trigger words set apparently")
        
        return False
        
    def get_link(self):
        """
        Query cat URL to get a random link
        """
        try:
            link_url = self.registryValue('linkURL')
            response = utils.web.getUrl(link_url).decode('utf8')
            
            # Expecting a link
            if "http" in response:
                return response
            else:
                self.log.error("Cayenne: received unexpected response from cat URL: %s" % (response))
            
        except:
            self.log.exception("Cayenne: error fetching cat URL")
    
    def doPrivmsg(self, irc, msg):
        """
        Checks each channel message to see if it contains a trigger word
        """
        channel = msg.args[0]
        is_channel = irc.isChannel(channel)
        is_ctcp = ircmsgs.isCtcp(msg)        
        message = msg.args[1]
        
        # Check origin nick to make sure the trigger
        # didn't come from the bot.
        origin_nick = msg.nick
        
        # Only react to messages/actions in a channel
        if is_channel and not is_ctcp:            
            if type(message) is str and len(message):
                fact_chance = int(self.registryValue('factChance'))
                link_chance = int(self.registryValue('linkChance'))            
                throttle_seconds = int(self.registryValue('throttleInSeconds'))
                triggered = self.message_contains_trigger_word(message)
                now = datetime.datetime.now()
                seconds = 0
                
                if self.last_message_timestamp:                
                    seconds = (now - self.last_message_timestamp).total_seconds()
                    throttled = seconds < throttle_seconds
                else:
                    throttled = False
                
                if triggered is not False:
                    self.log.debug("Cayenne triggered because message contained %s" % (triggered))
                    
                    if throttled:                    
                        self.log.info("Cayenne throttled. Not meowing: it has been %s seconds" % (seconds))
                    else:
                        fact_rand = random.randrange(0, 100) < fact_chance
                        link_rand = random.randrange(0, 100) < link_chance
                        
                        if fact_rand or link_rand:
                            self.last_message_timestamp = now
                            
                            if fact_rand:
                                output = self.get_fact()
                            
                            if link_rand:
                                output = self.get_link()
                            
                            if output:
                                irc.reply(output)
                            else:
                                self.log.error("Cayenne: error retrieving output")
    
Class = Cayenne


