# bhUtilities.py
# (C) Brendan J. Herger
# Analytics Master's Candidate at University of San Francisco
# 13herger@gmail.com
#
# Available under MIT License
# http://opensource.org/licenses/MIT
#
#*********************************
import multiprocessing
import datetime
import urllib2

__author__ = 'bjherger'

# imports
############################################

import matplotlib.pyplot as plt

import os
import cPickle as pickle
import re
import sys
import time
import functools
from xml.dom.minidom import parse

import numpy as np

# import sys
# sys.stdout = open('2.6_Beer.txt', 'w')

#variables
############################################

STOP_WORDS = set([ "as", "able", "about", "above", "according", "accordingly", "across", "actually", "after", "afterwards", "again", "against", "aint", "all", "allow", "allows", "almost", "alone", "along", "already", "also", "although", "always", "am", "among", "amongst", "an", "and", "another", "any", "anybody", "anyhow", "anyone", "anything", "anyway", "anyways", "anywhere", "apart", "appear", "appreciate", "appropriate", "are", "arent", "around", "as", "aside", "ask", "asking", "associated", "at", "available", "away", "awfully", "be", "became", "because", "become", "becomes", "becoming", "been", "before", "beforehand", "behind", "being", "believe", "below", "beside", "besides", "best", "better", "between", "beyond", "both", "brief", "but", "by", "cmon", "cs", "came", "can", "cant", "cannot", "cant", "cause", "causes", "certain", "certainly", "changes", "clearly", "co", "com", "come", "comes", "concerning", "consequently", "consider", "considering", "contain", "containing", "contains", "corresponding", "could", "couldnt", "course", "currently", "definitely", "described", "despite", "did", "didnt", "different", "do", "does", "doesnt", "doing", "dont", "done", "down", "downwards", "during", "each", "edu", "eg", "eight", "either", "else", "elsewhere", "enough", "entirely", "especially", "et", "etc", "even", "ever", "every", "everybody", "everyone", "everything", "everywhere", "ex", "exactly", "example", "except", "far", "few", "fifth", "first", "five", "followed", "following", "follows", "for", "former", "formerly", "forth", "four", "from", "further", "furthermore", "get", "gets", "getting", "given", "gives", "go", "goes", "going", "gone", "got", "gotten", "greetings", "had", "hadnt", "happens", "hardly", "has", "hasnt", "have", "havent", "having", "he", "hes", "hello", "help", "hence", "her", "here", "heres", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "hi", "him", "himself", "his", "hither", "hopefully", "how", "howbeit", "however", "id", "ill", "im", "ive", "ie", "if", "ignored", "immediate", "in", "inasmuch", "inc", "indeed", "indicate", "indicated", "indicates", "inner", "insofar", "instead", "into", "inward", "is", "isnt", "it", "itd", "itll", "its", "its", "itself", "just", "keep", "keeps", "kept", "know", "known", "knows", "last", "lately", "later", "latter", "latterly", "least", "less", "lest", "let", "lets", "like", "liked", "likely", "little", "look", "looking", "looks", "ltd", "mainly", "many", "may", "maybe", "me", "mean", "meanwhile", "merely", "might", "more", "moreover", "most", "mostly", "much", "must", "my", "myself", "name", "namely", "nd", "near", "nearly", "necessary", "need", "needs", "neither", "never", "nevertheless", "new", "next", "nine", "no", "nobody", "non", "none", "noone", "nor", "normally", "not", "nothing", "novel", "now", "nowhere", "obviously", "of", "off", "often", "oh", "ok", "okay", "old", "on", "once", "one", "ones", "only", "onto", "or", "other", "others", "otherwise", "ought", "our", "ours", "ourselves", "out", "outside", "over", "overall", "own", "particular", "particularly", "per", "perhaps", "placed", "please", "plus", "possible", "presumably", "probably", "provides", "que", "quite", "qv", "rather", "rd", "re", "really", "reasonably", "regarding", "regardless", "regards", "relatively", "respectively", "right", "said", "same", "saw", "say", "saying", "says", "second", "secondly", "see", "seeing", "seem", "seemed", "seeming", "seems", "seen", "self", "selves", "sensible", "sent", "serious", "seriously", "seven", "several", "shall", "she", "should", "shouldnt", "since", "six", "so", "some", "somebody", "somehow", "someone", "something", "sometime", "sometimes", "somewhat", "somewhere", "soon", "sorry", "specified", "specify", "specifying", "still", "sub", "such", "sup", "sure", "ts", "take", "taken", "tell", "tends", "th", "than", "thank", "thanks", "thanx", "that", "thats", "thats", "the", "their", "theirs", "them", "themselves", "then", "thence", "there", "theres", "thereafter", "thereby", "therefore", "therein", "theres", "thereupon", "these", "they", "theyd", "theyll", "theyre", "theyve", "think", "third", "this", "thorough", "thoroughly", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "took", "toward", "towards", "tried", "tries", "truly", "try", "trying", "twice", "two", "un", "under", "unfortunately", "unless", "unlikely", "until", "unto", "up", "upon", "us", "use", "used", "useful", "uses", "using", "usually", "value", "various", "very", "via", "viz", "vs", "want", "wants", "was", "wasnt", "way", "we", "wed", "well", "were", "weve", "welcome", "well", "went", "were", "werent", "what", "whats", "whatever", "when", "whence", "whenever", "where", "wheres", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whos", "whoever", "whole", "whom", "whose", "why", "will", "willing", "wish", "with", "within", "without", "wont", "wonder", "would", "wouldnt", "yes", "yet", "you", "youd", "youll", "youre", "youve", "your", "yours", "yourself", "yourselves", "zero"])

# courtesy http://www3.nd.edu/~mcdonald/Word_Lists.html
POS_WORDS = set(["able", "abundance", "abundant", "acclaimed", "accomplish", "accomplished", "accomplishes", "accomplishing", "accomplishment", "accomplishments", "achieve", "achieved", "achievement", "achievements", "achieves", "achieving", "adequately", "advancement", "advancements", "advances", "advancing", "advantage", "advantaged", "advantageous", "advantageously", "advantages", "alliance", "alliances", "assure", "assured", "assures", "assuring", "attain", "attained", "attaining", "attainment", "attainments", "attains", "attractive", "attractiveness", "beautiful", "beautifully", "beneficial", "beneficially", "benefit", "benefited", "benefiting", "benefitted", "benefitting", "best", "better", "bolstered", "bolstering", "bolsters", "boom", "booming", "boost", "boosted", "breakthrough", "breakthroughs", "brilliant", "charitable", "collaborate", "collaborated", "collaborates", "collaborating", "collaboration", "collaborations", "collaborative", "collaborator", "collaborators", "compliment", "complimentary", "complimented", "complimenting", "compliments", "conclusive", "conclusively", "conducive", "confident", "constructive", "constructively", "courteous", "creative", "creatively", "creativeness", "creativity", "delight", "delighted", "delightful", "delightfully", "delighting", "delights", "dependability", "dependable", "desirable", "desired", "despite", "destined", "diligent", "diligently", "distinction", "distinctions", "distinctive", "distinctively", "distinctiveness", "dream", "easier", "easily", "easy", "effective", "efficiencies", "efficiency", "efficient", "efficiently", "empower", "empowered", "empowering", "empowers", "enable", "enabled", "enables", "enabling", "encouraged", "encouragement", "encourages", "encouraging", "enhance", "enhanced", "enhancement", "enhancements", "enhances", "enhancing", "enjoy", "enjoyable", "enjoyably", "enjoyed", "enjoying", "enjoyment", "enjoys", "enthusiasm", "enthusiastic", "enthusiastically", "excellence", "excellent", "excelling", "excels", "exceptional", "exceptionally", "excited", "excitement", "exciting", "exclusive", "exclusively", "exclusiveness", "exclusives", "exclusivity", "exemplary", "fantastic", "favorable", "favorably", "favored", "favoring", "favorite", "favorites", "friendly", "gain", "gained", "gaining", "gains", "good", "great", "greater", "greatest", "greatly", "greatness", "happiest", "happily", "happiness", "happy", "highest", "honor", "honorable", "honored", "honoring", "honors", "ideal", "impress", "impressed", "impresses", "impressing", "impressive", "impressively", "improve", "improved", "improvement", "improvements", "improves", "improving", "incredible", "incredibly", "influential", "informative", "ingenuity", "innovate", "innovated", "innovates", "innovating", "innovation", "innovations", "innovative", "innovativeness", "innovator", "innovators", "insightful", "inspiration", "inspirational", "integrity", "invent", "invented", "inventing", "invention", "inventions", "inventive", "inventiveness", "inventor", "inventors", "leadership", "leading", "loyal", "lucrative", "meritorious", "opportunities", "opportunity", "optimistic", "outperform", "outperformed", "outperforming", "outperforms", "perfect", "perfected", "perfectly", "perfects", "pleasant", "pleasantly", "pleased", "pleasure", "plentiful", "popular", "popularity", "positive", "positively", "preeminence", "preeminent", "premier", "premiere", "prestige", "prestigious", "proactive", "proactively", "proficiency", "proficient", "proficiently", "profitability", "profitable", "profitably", "progress", "progressed", "progresses", "progressing", "prospered", "prospering", "prosperity", "prosperous", "prospers", "rebound", "rebounded", "rebounding", "receptive", "regain", "regained", "regaining", "resolve", "revolutionize", "revolutionized", "revolutionizes", "revolutionizing", "reward", "rewarded", "rewarding", "rewards", "satisfaction", "satisfactorily", "satisfactory", "satisfied", "satisfies", "satisfy", "satisfying", "smooth", "smoothing", "smoothly", "smooths", "solves", "solving", "spectacular", "spectacularly", "stability", "stabilization", "stabilizations", "stabilize", "stabilized", "stabilizes", "stabilizing", "stable", "strength", "strengthen", "strengthened", "strengthening", "strengthens", "strengths", "strong", "stronger", "strongest", "succeed", "succeeded", "succeeding", "succeeds", "success", "successes", "successful", "successfully", "superior", "surpass", "surpassed", "surpasses", "surpassing", "transparency", "tremendous", "tremendously", "unmatched", "unparalleled", "unsurpassed", "upturn", "upturns", "valuable", "versatile", "versatility", "vibrancy", "vibrant", "win", "winner", "winners", "winning", "worthy" ])
NEG_WORDS = set(["abandon", "abandoned", "abandoning", "abandonment", "abandonments", "abandons", "abdicated", "abdicates", "abdicating", "abdication", "abdications", "aberrant", "aberration", "aberrational", "aberrations", "abetting", "abnormal", "abnormalities", "abnormality", "abnormally", "abolish", "abolished", "abolishes", "abolishing", "abrogate", "abrogated", "abrogates", "abrogating", "abrogation", "abrogations", "abrupt", "abruptly", "abruptness", "absence", "absences", "absenteeism", "abuse", "abused", "abuses", "abusing", "abusive", "abusively", "abusiveness", "accident", "accidental", "accidentally", "accidents", "accusation", "accusations", "accuse", "accused", "accuses", "accusing", "acquiesce", "acquiesced", "acquiesces", "acquiescing", "acquit", "acquits", "acquittal", "acquittals", "acquitted", "acquitting", "adulterate", "adulterated", "adulterating", "adulteration", "adulterations", "adversarial", "adversaries", "adversary", "adverse", "adversely", "adversities", "adversity", "aftermath", "aftermaths", "against", "aggravate", "aggravated", "aggravates", "aggravating", "aggravation", "aggravations", "alerted", "alerting", "alienate", "alienated", "alienates", "alienating", "alienation", "alienations", "allegation", "allegations", "allege", "alleged", "allegedly", "alleges", "alleging", "annoy", "annoyance", "annoyances", "annoyed", "annoying", "annoys", "annul", "annulled", "annulling", "annulment", "annulments", "annuls", "anomalies", "anomalous", "anomalously", "anomaly", "anticompetitive", "antitrust", "argue", "argued", "arguing", "argument", "argumentative", "arguments", "arrearage", "arrearages", "arrears", "arrest", "arrested", "arrests", "artificially", "assault", "assaulted", "assaulting", "assaults", "assertions", "attrition", "aversely", "backdating", "bad", "bail", "bailout", "balk", "balked", "bankrupt", "bankruptcies", "bankruptcy", "bankrupted", "bankrupting", "bankrupts", "bans", "barred", "barrier", "barriers", "bottleneck", "bottlenecks", "boycott", "boycotted", "boycotting", "boycotts", "breach", "breached", "breaches", "breaching", "break", "breakage", "breakages", "breakdown", "breakdowns", "breaking", "breaks", "bribe", "bribed", "briberies", "bribery", "bribes", "bribing", "bridge", "broken", "burden", "burdened", "burdening", "burdens", "burdensome", "burned", "calamities", "calamitous", "calamity", "cancel", "canceled", "canceling", "cancellation", "cancellations", "cancelled", "cancelling", "cancels", "careless", "carelessly", "carelessness", "catastrophe", "catastrophes", "catastrophic", "catastrophically", "caution", "cautionary", "cautioned", "cautioning", "cautions", "cease", "ceased", "ceases", "ceasing", "censure", "censured", "censures", "censuring", "challenge", "challenged", "challenges", "challenging", "chargeoffs", "circumvent", "circumvented", "circumventing", "circumvention", "circumventions", "circumvents", "claiming", "claims", "clawback", "closed", "closeout", "closeouts", "closing", "closings", "closure", "closures", "coerce", "coerced", "coerces", "coercing", "coercion", "coercive", "collapse", "collapsed", "collapses", "collapsing", "collision", "collisions", "collude", "colluded", "colludes", "colluding", "collusion", "collusions", "collusive", "complain", "complained", "complaining", "complains", "complaint", "complaints", "complicate", "complicated", "complicates", "complicating", "complication", "complications", "compulsion", "concealed", "concealing", "concede", "conceded", "concedes", "conceding", "concern", "concerned", "concerns", "conciliating", "conciliation", "conciliations", "condemn", "condemnation", "condemnations", "condemned", "condemning", "condemns", "condone", "condoned", "confess", "confessed", "confesses", "confessing", "confession", "confine", "confined", "confinement", "confinements", "confines", "confining", "confiscate", "confiscated", "confiscates", "confiscating", "confiscation", "confiscations", "conflict", "conflicted", "conflicting", "conflicts", "confront", "confrontation", "confrontational", "confrontations", "confronted", "confronting", "confronts", "confuse", "confused", "confuses", "confusing", "confusingly", "confusion", "conspiracies", "conspiracy", "conspirator", "conspiratorial", "conspirators", "conspire", "conspired", "conspires", "conspiring", "contempt", "contend", "contended", "contending", "contends", "contention", "contentions", "contentious", "contentiously", "contested", "contesting", "contraction", "contractions", "contradict", "contradicted", "contradicting", "contradiction", "contradictions", "contradictory", "contradicts", "contrary", "controversial", "controversies", "controversy", "convict", "convicted", "convicting", "conviction", "convictions", "corrected", "correcting", "correction", "corrections", "corrects", "corrupt", "corrupted", "corrupting", "corruption", "corruptions", "corruptly", "corruptness", "costly", "counterclaim", "counterclaimed", "counterclaiming", "counterclaims", "counterfeit", "counterfeited", "counterfeiter", "counterfeiters", "counterfeiting", "counterfeits", "countermeasure", "countermeasures", "crime", "crimes", "criminal", "criminally", "criminals", "crises", "crisis", "critical", "critically", "criticism", "criticisms", "criticize", "criticized", "criticizes", "criticizing", "crucial", "crucially", "culpability", "culpable", "culpably", "cumbersome", "curtail", "curtailed", "curtailing", "curtailment", "curtailments", "curtails", "cut", "cutback", "cutbacks", "damage", "damaged", "damages", "damaging", "dampen", "dampened", "danger", "dangerous", "dangerously", "dangers", "deadlock", "deadlocked", "deadlocking", "deadlocks", "deadweight", "deadweights", "debarment", "debarments", "debarred", "deceased", "deceit", "deceitful", "deceitfulness", "deceive", "deceived", "deceives", "deceiving", "deception", "deceptions", "deceptive", "deceptively", "decline", "declined", "declines", "declining", "deface", "defaced", "defacement", "defamation", "defamations", "defamatory", "defame", "defamed", "defames", "defaming", "default", "defaulted", "defaulting", "defaults", "defeat", "defeated", "defeating", "defeats", "defect", "defective", "defects", "defend", "defendant", "defendants", "defended", "defending", "defends", "defensive", "defer", "deficiencies", "deficiency", "deficient", "deficit", "deficits", "defraud", "defrauded", "defrauding", "defrauds", "defunct", "degradation", "degradations", "degrade", "degraded", "degrades", "degrading", "delay", "delayed", "delaying", "delays", "deleterious", "deliberate", "deliberated", "deliberately", "delinquencies", "delinquency", "delinquent", "delinquently", "delinquents", "delist", "delisted", "delisting", "delists", "demise", "demised", "demises", "demising", "demolish", "demolished", "demolishes", "demolishing", "demolition", "demolitions", "demote", "demoted", "demotes", "demoting", "demotion", "demotions", "denial", "denials", "denied", "denies", "denigrate", "denigrated", "denigrates", "denigrating", "denigration", "deny", "denying", "deplete", "depleted", "depletes", "depleting", "depletion", "depletions", "deprecation", "depress", "depressed", "depresses", "depressing", "deprivation", "deprive", "deprived", "deprives", "depriving", "derelict", "dereliction", "derogatory", "destabilization", "destabilize", "destabilized", "destabilizing", "destroy", "destroyed", "destroying", "destroys", "destruction", "destructive", "detain", "detained", "detention", "detentions", "deter", "deteriorate", "deteriorated", "deteriorates", "deteriorating", "deterioration", "deteriorations", "deterred", "deterrence", "deterrences", "deterrent", "deterrents", "deterring", "deters", "detract", "detracted", "detracting", "detriment", "detrimental", "detrimentally", "detriments", "devalue", "devalued", "devalues", "devaluing", "devastate", "devastated", "devastating", "devastation", "deviate", "deviated", "deviates", "deviating", "deviation", "deviations", "devolve", "devolved", "devolves", "devolving", "difficult", "difficulties", "difficultly", "difficulty", "diminish", "diminished", "diminishes", "diminishing", "diminution", "disadvantage", "disadvantaged", "disadvantageous", "disadvantages", "disaffiliation", "disagree", "disagreeable", "disagreed", "disagreeing", "disagreement", "disagreements", "disagrees", "disallow", "disallowance", "disallowances", "disallowed", "disallowing", "disallows", "disappear", "disappearance", "disappearances", "disappeared", "disappearing", "disappears", "disappoint", "disappointed", "disappointing", "disappointingly", "disappointment", "disappointments", "disappoints", "disapproval", "disapprovals", "disapprove", "disapproved", "disapproves", "disapproving", "disassociates", "disassociating", "disassociation", "disassociations", "disaster", "disasters", "disastrous", "disastrously", "disavow", "disavowal", "disavowed", "disavowing", "disavows", "disciplinary", "disclaim", "disclaimed", "disclaimer", "disclaimers", "disclaiming", "disclaims", "disclose", "disclosed", "discloses", "disclosing", "discontinuance", "discontinuances", "discontinuation", "discontinuations", "discontinue", "discontinued", "discontinues", "discontinuing", "discourage", "discouraged", "discourages", "discouraging", "discredit", "discredited", "discrediting", "discredits", "discrepancies", "discrepancy", "disfavor", "disfavored", "disfavoring", "disfavors", "disgorge", "disgorged", "disgorgement", "disgorgements", "disgorges", "disgorging", "disgrace", "disgraceful", "disgracefully", "dishonest", "dishonestly", "dishonesty", "dishonor", "dishonorable", "dishonorably", "dishonored", "dishonoring", "dishonors", "disincentives", "disinterested", "disinterestedly", "disinterestedness", "disloyal", "disloyally", "disloyalty", "dismal", "dismally", "dismiss", "dismissal", "dismissals", "dismissed", "dismisses", "dismissing", "disorderly", "disparage", "disparaged", "disparagement", "disparagements", "disparages", "disparaging", "disparagingly", "disparities", "disparity", "displace", "displaced", "displacement", "displacements", "displaces", "displacing", "dispose", "dispossess", "dispossessed", "dispossesses", "dispossessing", "disproportion", "disproportional", "disproportionate", "disproportionately", "dispute", "disputed", "disputes", "disputing", "disqualification", "disqualifications", "disqualified", "disqualifies", "disqualify", "disqualifying", "disregard", "disregarded", "disregarding", "disregards", "disreputable", "disrepute", "disrupt", "disrupted", "disrupting", "disruption", "disruptions", "disruptive", "disrupts", "dissatisfaction", "dissatisfied", "dissent", "dissented", "dissenter", "dissenters", "dissenting", "dissents", "dissident", "dissidents", "dissolution", "dissolutions", "distort", "distorted", "distorting", "distortion", "distortions", "distorts", "distract", "distracted", "distracting", "distraction", "distractions", "distracts", "distress", "distressed", "disturb", "disturbance", "disturbances", "disturbed", "disturbing", "disturbs", "diversion", "divert", "diverted", "diverting", "diverts", "divest", "divested", "divesting", "divestiture", "divestitures", "divestment", "divestments", "divests", "divorce", "divorced", "divulge", "divulged", "divulges", "divulging", "doubt", "doubted", "doubtful", "doubts", "downgrade", "downgraded", "downgrades", "downgrading", "downsize", "downsized", "downsizes", "downsizing", "downsizings", "downtime", "downtimes", "downturn", "downturns", "downward", "downwards", "drag", "drastic", "drastically", "drawback", "drawbacks", "dropped", "drought", "droughts", "duress", "dysfunction", "dysfunctional", "dysfunctions", "easing", "egregious", "egregiously", "embargo", "embargoed", "embargoes", "embargoing", "embarrass", "embarrassed", "embarrasses", "embarrassing", "embarrassment", "embarrassments", "embezzle", "embezzled", "embezzlement", "embezzlements", "embezzler", "embezzles", "embezzling", "encroach", "encroached", "encroaches", "encroaching", "encroachment", "encroachments", "encumber", "encumbered", "encumbering", "encumbers", "encumbrance", "encumbrances", "endanger", "endangered", "endangering", "endangerment", "endangers", "enjoin", "enjoined", "enjoining", "enjoins", "erode", "eroded", "erodes", "eroding", "erosion", "erratic", "erratically", "erred", "erring", "erroneous", "erroneously", "error", "errors", "errs", "escalate", "escalated", "escalates", "escalating", "evade", "evaded", "evades", "evading", "evasion", "evasions", "evasive", "evict", "evicted", "evicting", "eviction", "evictions", "evicts", "exacerbate", "exacerbated", "exacerbates", "exacerbating", "exacerbation", "exacerbations", "exaggerate", "exaggerated", "exaggerates", "exaggerating", "exaggeration", "excessive", "excessively", "exculpate", "exculpated", "exculpates", "exculpating", "exculpation", "exculpations", "exculpatory", "exonerate", "exonerated", "exonerates", "exonerating", "exoneration", "exonerations", "exploit", "exploitation", "exploitations", "exploitative", "exploited", "exploiting", "exploits", "expose", "exposed", "exposes", "exposing", "expropriate", "expropriated", "expropriates", "expropriating", "expropriation", "expropriations", "expulsion", "expulsions", "extenuating", "fail", "failed", "failing", "failings", "fails", "failure", "failures", "fallout", "false", "falsely", "falsification", "falsifications", "falsified", "falsifies", "falsify", "falsifying", "falsity", "fatalities", "fatality", "fatally", "fault", "faulted", "faults", "faulty", "fear", "fears", "felonies", "felonious", "felony", "fictitious", "fined", "fines", "fired", "firing", "flaw", "flawed", "flaws", "forbid", "forbidden", "forbidding", "forbids", "force", "forced", "forcing", "foreclose", "foreclosed", "forecloses", "foreclosing", "foreclosure", "foreclosures", "forego", "foregoes", "foregone", "forestall", "forestalled", "forestalling", "forestalls", "forfeit", "forfeited", "forfeiting", "forfeits", "forfeiture", "forfeitures", "forgers", "forgery", "fraud", "frauds", "fraudulence", "fraudulent", "fraudulently", "frivolous", "frivolously", "frustrate", "frustrated", "frustrates", "frustrating", "frustratingly", "frustration", "frustrations", "fugitive", "fugitives", "gratuitous", "gratuitously", "grievance", "grievances", "grossly", "groundless", "guilty", "halt", "halted", "hamper", "hampered", "hampering", "hampers", "harass", "harassed", "harassing", "harassment", "hardship", "hardships", "harm", "harmed", "harmful", "harmfully", "harming", "harms", "harsh", "harsher", "harshest", "harshly", "harshness", "hazard", "hazardous", "hazards", "hinder", "hindered", "hindering", "hinders", "hindrance", "hindrances", "hostile", "hostility", "hurt", "hurting", "idle", "idled", "idling", "ignore", "ignored", "ignores", "ignoring", "ill", "illegal", "illegalities", "illegality", "illegally", "illegible", "illicit", "illicitly", "illiquid", "illiquidity", "imbalance", "imbalances", "immature", "immoral", "impair", "impaired", "impairing", "impairment", "impairments", "impairs", "impasse", "impasses", "impede", "impeded", "impedes", "impediment", "impediments", "impeding", "impending", "imperative", "imperfection", "imperfections", "imperil", "impermissible", "implicate", "implicated", "implicates", "implicating", "impossibility", "impossible", "impound", "impounded", "impounding", "impounds", "impracticable", "impractical", "impracticalities", "impracticality", "imprisonment", "improper", "improperly", "improprieties", "impropriety", "imprudent", "imprudently", "inability", "inaccessible", "inaccuracies", "inaccuracy", "inaccurate", "inaccurately", "inaction", "inactions", "inactivate", "inactivated", "inactivates", "inactivating", "inactivation", "inactivations", "inactivity", "inadequacies", "inadequacy", "inadequate", "inadequately", "inadvertent", "inadvertently", "inadvisability", "inadvisable", "inappropriate", "inappropriately", "inattention", "incapable", "incapacitated", "incapacity", "incarcerate", "incarcerated", "incarcerates", "incarcerating", "incarceration", "incarcerations", "incidence", "incidences", "incident", "incidents", "incompatibilities", "incompatibility", "incompatible", "incompetence", "incompetency", "incompetent", "incompetently", "incompetents", "incomplete", "incompletely", "incompleteness", "inconclusive", "inconsistencies", "inconsistency", "inconsistent", "inconsistently", "inconvenience", "inconveniences", "inconvenient", "incorrect", "incorrectly", "incorrectness", "indecency", "indecent", "indefeasible", "indefeasibly", "indict", "indictable", "indicted", "indicting", "indictment", "indictments", "ineffective", "ineffectively", "ineffectiveness", "inefficiencies", "inefficiency", "inefficient", "inefficiently", "ineligibility", "ineligible", "inequitable", "inequitably", "inequities", "inequity", "inevitable", "inexperience", "inexperienced", "inferior", "inflicted", "infraction", "infractions", "infringe", "infringed", "infringement", "infringements", "infringes", "infringing", "inhibited", "inimical", "injunction", "injunctions", "injure", "injured", "injures", "injuries", "injuring", "injurious", "injury", "inordinate", "inordinately", "inquiry", "insecure", "insensitive", "insolvencies", "insolvency", "insolvent", "instability", "insubordination", "insufficiency", "insufficient", "insufficiently", "insurrection", "insurrections", "intentional", "interfere", "interfered", "interference", "interferences", "interferes", "interfering", "intermittent", "intermittently", "interrupt", "interrupted", "interrupting", "interruption", "interruptions", "interrupts", "intimidation", "intrusion", "invalid", "invalidate", "invalidated", "invalidates", "invalidating", "invalidation", "invalidity", "investigate", "investigated", "investigates", "investigating", "investigation", "investigations", "involuntarily", "involuntary", "irreconcilable", "irreconcilably", "irrecoverable", "irrecoverably", "irregular", "irregularities", "irregularity", "irregularly", "irreparable", "irreparably", "irreversible", "jeopardize", "jeopardized", "justifiable", "kickback", "kickbacks", "knowingly", "lack", "lacked", "lacking", "lackluster", "lacks", "lag", "lagged", "lagging", "lags", "lapse", "lapsed", "lapses", "lapsing", "late", "laundering", "layoff", "layoffs", "lie", "limitation", "limitations", "lingering", "liquidate", "liquidated", "liquidates", "liquidating", "liquidation", "liquidations", "liquidator", "liquidators", "litigant", "litigants", "litigate", "litigated", "litigates", "litigating", "litigation", "litigations", "lockout", "lockouts", "lose", "loses", "losing", "loss", "losses", "lost", "lying", "malfeasance", "malfunction", "malfunctioned", "malfunctioning", "malfunctions", "malice", "malicious", "maliciously", "malpractice", "manipulate", "manipulated", "manipulates", "manipulating", "manipulation", "manipulations", "manipulative", "markdown", "markdowns", "misapplication", "misapplications", "misapplied", "misapplies", "misapply", "misapplying", "misappropriate", "misappropriated", "misappropriates", "misappropriating", "misappropriation", "misappropriations", "misbranded", "miscalculate", "miscalculated", "miscalculates", "miscalculating", "miscalculation", "miscalculations", "mischief", "misclassification", "misclassified", "misconduct", "misdated", "misdemeanor", "misdemeanors", "misdirected", "mishandle", "mishandled", "mishandles", "mishandling", "misinform", "misinformation", "misinformed", "misinforming", "misinforms", "misinterpret", "misinterpretation", "misinterpretations", "misinterpreted", "misinterpreting", "misinterprets", "misjudge", "misjudged", "misjudges", "misjudging", "misjudgment", "misjudgments", "mislabel", "mislabeled", "mislabeling", "mislabelled", "mislabels", "mislead", "misleading", "misleadingly", "misleads", "misled", "mismanage", "mismanaged", "mismanagement", "mismanages", "mismanaging", "mismatch", "mismatched", "mismatches", "mismatching", "misplaced", "misrepresent", "misrepresentation", "misrepresentations", "misrepresented", "misrepresenting", "misrepresents", "miss", "missed", "misses", "misstate", "misstated", "misstatement", "misstatements", "misstates", "misstating", "misstep", "missteps", "mistake", "mistaken", "mistakenly", "mistakes", "mistaking", "mistrial", "mistrials", "misunderstand", "misunderstanding", "misunderstandings", "misunderstood", "misuse", "misused", "misuses", "misusing", "monopolistic", "monopolists", "monopolization", "monopolize", "monopolized", "monopolizes", "monopolizing", "monopoly", "moratoria", "moratorium", "moratoriums", "mothballed", "mothballing", "negative", "negatively", "negatives", "neglect", "neglected", "neglectful", "neglecting", "neglects", "negligence", "negligences", "negligent", "negligently", "nonattainment", "noncompetitive", "noncompliance", "noncompliances", "noncompliant", "noncomplying", "nonconforming", "nonconformities", "nonconformity", "nondisclosure", "nonfunctional", "nonpayment", "nonpayments", "nonperformance", "nonperformances", "nonperforming", "nonproducing", "nonproductive", "nonrecoverable", "nonrenewal", "nuisance", "nuisances", "nullification", "nullifications", "nullified", "nullifies", "nullify", "nullifying", "objected", "objecting", "objection", "objectionable", "objectionably", "objections", "obscene", "obscenity", "obsolescence", "obsolete", "obstacle", "obstacles", "obstruct", "obstructed", "obstructing", "obstruction", "obstructions", "offence", "offences", "offend", "offended", "offender", "offenders", "offending", "offends", "omission", "omissions", "omit", "omits", "omitted", "omitting", "onerous", "opportunistic", "opportunistically", "oppose", "opposed", "opposes", "opposing", "opposition", "oppositions", "outage", "outages", "outdated", "outmoded", "overage", "overages", "overbuild", "overbuilding", "overbuilds", "overbuilt", "overburden", "overburdened", "overburdening", "overcapacities", "overcapacity", "overcharge", "overcharged", "overcharges", "overcharging", "overcome", "overcomes", "overcoming", "overdue", "overestimate", "overestimated", "overestimates", "overestimating", "overestimation", "overestimations", "overload", "overloaded", "overloading", "overloads", "overlook", "overlooked", "overlooking", "overlooks", "overpaid", "overpayment", "overpayments", "overproduced", "overproduces", "overproducing", "overproduction", "overrun", "overrunning", "overruns", "overshadow", "overshadowed", "overshadowing", "overshadows", "overstate", "overstated", "overstatement", "overstatements", "overstates", "overstating", "oversupplied", "oversupplies", "oversupply", "oversupplying", "overtly", "overturn", "overturned", "overturning", "overturns", "overvalue", "overvalued", "overvaluing", "panic", "panics", "penalize", "penalized", "penalizes", "penalizing", "penalties", "penalty", "peril", "perils", "perjury", "perpetrate", "perpetrated", "perpetrates", "perpetrating", "perpetration", "persist", "persisted", "persistence", "persistent", "persistently", "persisting", "persists", "pervasive", "pervasively", "pervasiveness", "petty", "picket", "picketed", "picketing", "plaintiff", "plaintiffs", "plea", "plead", "pleaded", "pleading", "pleadings", "pleads", "pleas", "pled", "poor", "poorly", "poses", "posing", "postpone", "postponed", "postponement", "postponements", "postpones", "postponing", "precipitated", "precipitous", "precipitously", "preclude", "precluded", "precludes", "precluding", "predatory", "prejudice", "prejudiced", "prejudices", "prejudicial", "prejudicing", "premature", "prematurely", "pressing", "pretrial", "preventing", "prevention", "prevents", "problem", "problematic", "problematical", "problems", "prolong", "prolongation", "prolongations", "prolonged", "prolonging", "prolongs", "prone", "prosecute", "prosecuted", "prosecutes", "prosecuting", "prosecution", "prosecutions", "protest", "protested", "protester", "protesters", "protesting", "protestor", "protestors", "protests", "protracted", "protraction", "provoke", "provoked", "provokes", "provoking", "punished", "punishes", "punishing", "punishment", "punishments", "punitive", "purport", "purported", "purportedly", "purporting", "purports", "question", "questionable", "questionably", "questioned", "questioning", "questions", "quit", "quitting", "racketeer", "racketeering", "rationalization", "rationalizations", "rationalize", "rationalized", "rationalizes", "rationalizing", "reassessment", "reassessments", "reassign", "reassigned", "reassigning", "reassignment", "reassignments", "reassigns", "recall", "recalled", "recalling", "recalls", "recession", "recessionary", "recessions", "reckless", "recklessly", "recklessness", "redact", "redacted", "redacting", "redaction", "redactions", "redefaulted", "redress", "redressed", "redresses", "redressing", "refusal", "refusals", "refuse", "refused", "refuses", "refusing", "reject", "rejected", "rejecting", "rejection", "rejections", "rejects", "relinquish", "relinquished", "relinquishes", "relinquishing", "relinquishment", "relinquishments", "reluctance", "reluctant", "renegotiate", "renegotiated", "renegotiates", "renegotiating", "renegotiation", "renegotiations", "renounce", "renounced", "renouncement", "renouncements", "renounces", "renouncing", "reparation", "reparations", "repossessed", "repossesses", "repossessing", "repossession", "repossessions", "repudiate", "repudiated", "repudiates", "repudiating", "repudiation", "repudiations", "resign", "resignation", "resignations", "resigned", "resigning", "resigns", "restate", "restated", "restatement", "restatements", "restates", "restating", "restructure", "restructured", "restructures", "restructuring", "restructurings", "retaliate", "retaliated", "retaliates", "retaliating", "retaliation", "retaliations", "retaliatory", "retribution", "retributions", "revocation", "revocations", "revoke", "revoked", "revokes", "revoking", "ridicule", "ridiculed", "ridicules", "ridiculing", "riskier", "riskiest", "risky", "sabotage", "sacrifice", "sacrificed", "sacrifices", "sacrificial", "sacrificing", "scandalous", "scandals", "scrutinize", "scrutinized", "scrutinizes", "scrutinizing", "scrutiny", "secrecy", "seize", "seized", "seizes", "seizing", "sentenced", "sentencing", "serious", "seriously", "seriousness", "setback", "setbacks", "sever", "severe", "severed", "severely", "severities", "severity", "sharply", "shocked", "shortage", "shortages", "shortfall", "shortfalls", "shrinkage", "shrinkages", "shut", "shutdown", "shutdowns", "shuts", "shutting", "slander", "slandered", "slanderous", "slanders", "slippage", "slippages", "slow", "slowdown", "slowdowns", "slowed", "slower", "slowest", "slowing", "slowly", "slowness", "sluggish", "sluggishly", "sluggishness", "solvencies", "solvency", "staggering", "stagnant", "stagnate", "stagnated", "stagnates", "stagnating", "stagnation", "standstill", "standstills", "stolen", "stoppage", "stoppages", "stopped", "stopping", "stops", "strain", "strained", "straining", "strains", "stress", "stressed", "stresses", "stressful", "stressing", "stringent", "subjected", "subjecting", "subjection", "subpoena", "subpoenaed", "subpoenas", "substandard", "sue", "sued", "sues", "suffer", "suffered", "suffering", "suffers", "suing", "summoned", "summoning", "summons", "summonses", "susceptibility", "susceptible", "suspect", "suspected", "suspects", "suspend", "suspended", "suspending", "suspends", "suspension", "suspensions", "suspicion", "suspicions", "suspicious", "suspiciously", "taint", "tainted", "tainting", "taints", "tampered", "tense", "terminate", "terminated", "terminates", "terminating", "termination", "terminations", "testify", "testifying", "threat", "threaten", "threatened", "threatening", "threatens", "threats", "tightening", "tolerate", "tolerated", "tolerates", "tolerating", "toleration", "tortuous", "tortuously", "tragedies", "tragedy", "tragic", "tragically", "traumatic", "trouble", "troubled", "troubles", "turbulence", "turmoil", "unable", "unacceptable", "unacceptably", "unaccounted", "unannounced", "unanticipated", "unapproved", "unattractive", "unauthorized", "unavailability", "unavailable", "unavoidable", "unavoidably", "unaware", "uncollectable", "uncollected", "uncollectibility", "uncollectible", "uncollectibles", "uncompetitive", "uncompleted", "unconscionable", "unconscionably", "uncontrollable", "uncontrollably", "uncontrolled", "uncorrected", "uncover", "uncovered", "uncovering", "uncovers", "undeliverable", "undelivered", "undercapitalized", "undercut", "undercuts", "undercutting", "underestimate", "underestimated", "underestimates", "underestimating", "underestimation", "underfunded", "underinsured", "undermine", "undermined", "undermines", "undermining", "underpaid", "underpayment", "underpayments", "underpays", "underperform", "underperformance", "underperformed", "underperforming", "underproduced", "underproduction", "underreporting", "understate", "understated", "understatement", "understatements", "understates", "understating", "underutilization", "underutilized", "undesirable", "undesired", "undetected", "undetermined", "undisclosed", "undocumented", "undue", "unduly", "uneconomic", "uneconomical", "uneconomically", "unemployed", "unemployment", "unethical", "unethically", "unexcused", "unexpected", "unexpectedly", "unfair", "unfairly", "unfavorable", "unfavorably", "unfavourable", "unfeasible", "unfit", "unfitness", "unforeseeable", "unforeseen", "unforseen", "unfortunate", "unfortunately", "unfounded", "unfriendly", "unfulfilled", "unfunded", "uninsured", "unintended", "unintentional", "unintentionally", "unjust", "unjustifiable", "unjustifiably", "unjustified", "unjustly", "unknowing", "unknowingly", "unlawful", "unlawfully", "unlicensed", "unliquidated", "unmarketable", "unmerchantable", "unnecessarily", "unnecessary", "unneeded", "unobtainable", "unoccupied", "unpaid", "unperformed", "unplanned", "unpopular", "unpredictability", "unpredictable", "unpredictably", "unpredicted", "unproductive", "unprofitability", "unprofitable", "unqualified", "unrealistic", "unreasonable", "unreasonableness", "unreasonably", "unrecoverable", "unrecovered", "unreimbursed", "unreliable", "unremedied", "unreported", "unresolved", "unrest", "unsafe", "unsalable", "unsaleable", "unsatisfactory", "unsatisfied", "unsavory", "unscheduled", "unsold", "unsound", "unstable", "unsubstantiated", "unsuccessful", "unsuccessfully", "unsuitability", "unsuitable", "unsuitably", "unsuited", "unsure", "unsuspected", "unsuspecting", "unsustainable", "untenable", "untimely", "untruth", "untruthful", "untruthfully", "untruthfulness", "untruths", "unusable", "unwanted", "unwarranted", "unwelcome", "unwilling", "unwillingness", "upset", "urgency", "urgent", "usurious", "usurp", "usurped", "usurping", "usurps", "usury", "vandalism", "verdict", "verdicts", "vetoed", "victims", "violate", "violated", "violates", "violating", "violation", "violations", "violative", "violator", "violators", "violence", "violent", "violently", "vitiate", "vitiated", "vitiates", "vitiating", "vitiation", "voided", "voiding", "volatile", "volatility", "vulnerabilities", "vulnerability", "vulnerable", "vulnerably", "warn", "warned", "warning", "warnings", "warns", "wasted", "wasteful", "wasting", "weak", "weaken", "weakened", "weakening", "weakens", "weaker", "weakest", "weakly", "weakness", "weaknesses", "willfully", "worries", "worry", "worrying", "worse", "worsen", "worsened", "worsening", "worsens", "worst", "worthless", "writedown", "writedowns", "writeoff", "writeoffs", "wrong", "wrongdoing", "wrongdoings", "wrongful", "wrongfully", "wrongly" ])

separator = "\n*****************************"

START_TIME = None

STOUT_DEFAULT = sys.stdout
STOUT_DEVNULL = open(os.devnull,"w")

# functions
############################################

# functions - File I/O
############################################


def output_to_file(filename = "output.txt"):
    global STOUT_DEFAULT
    filename = str(datetime.datetime.now()) + " " + filename
    sys.stdout = open(filename, 'w')
    STOUT_DEFAULT = sys.stdout


def rejoin_list(list):
    """
    Flattens a list of lists. Non-recursive.
    :param list: list of form [ [...] , [...], ... ]
    :return: list of form [ ... ]
    """
    temp = []
    for elem in list:
        temp.extend(elem)
    return temp

def function_wrapper(function, list):
    STOUT_DEFAULT.write('.')
    return function(list)



def multi_map(function, sequence):

    #set up multiprocessing
    pool_size = multiprocessing.cpu_count() * 2
    pool = multiprocessing.Pool(processes=pool_size, maxtasksperchild=200)
    list_of_list_of_files = np.array_split(sequence, pool_size * 2)

    # multimap
    print "\nMapping"
    print "0%", "." * len(list_of_list_of_files), "100%"
    print "0% ",

    wrapped_function = functools.partial(function_wrapper, function)

    pool_outputs = pool.map(wrapped_function, list_of_list_of_files)

    # join threads
    pool.close()  # no more tasks
    pool.join()  # wrap up current tasks

    print "100%"
    print "\n"

    rejoined_outputs = rejoin_list(pool_outputs)

    return rejoined_outputs

# functions - File I/O
############################################
def read_file(filename):
    f = open(filename, 'r')
    return f.read()

def read_url(url):
    return urllib2.urlopen(url).read()


def readXMLByTag(file, tag):

    tag = str(tag)
    dom = parse(file)

    list = [node.childNodes[0].data for node in dom.getElementsByTagName(tag)]
    totalString = " "+ " ".join(list)+ " "
    return totalString


def traverseDirectory(directory):
    """
    *This implementation is specific to sub folders pos and neg within the directory*
    Recursively traverse the neg and pos subfolders of the given directory, and return the full path to any files
    contained within these subfolders
    :param directory: directory containing 'neg' and 'pos' subfolders
    :param subfolderList: list of subfolders to be searched separately. This likely maps to categories
    :return: (negativeFileArray, positiveFileArray)
    """
    clPath = directory
    clFiles = []
    for (dirpath, dirnames, filenames) in os.walk(clPath):
        local = [os.path.join(dirpath, file) for file in filenames]
        clFiles.extend(local)
    return clFiles


def loadPickle(file):
    try:
        # print "\nAttempting to load pkl file: ", file

        pkl_file = open(file, 'rb')
        toReturn = pickle.load(pkl_file)

        print "\n" + file + " LOADED."
        return toReturn

    #complie database if pickle unavailable, or unwanted.
    except:
        # print "\n  pkl file NOT LOADED"
        return None

        # output = open("move_unigram" +'.pkl', 'wb')
        # pickle.dump(masterDic, output)
        # output.close()


def savePickle(object, filename):
    try:
        # print "Attempting to pickle file: ", filename
        # print separator
        output = open(filename, 'wb')
        pickle.dump(object, output, -1)
        output.close()
        print "Done writing to pickle file: ", filename
    except:
        # print "Error pickling file: ", filename
        x = 0


# functions - Strings
############################################

def time_as_string():
    return str(time.asctime(time.gmtime()))

def re_match(pattern, string):
    match = re.findall(pattern, string)
    match = list(match)
    if len(match)>0:
        return match
    else:
        return None


def filterParameters(x):
    if len(x) <3:
        return False
    elif x in STOP_WORDS:
        return False
    else:
        return True


def splitAndCleanString(stringIn):
    """
    Splits a string and removes non-alpha numeric characters
    :param stringIn: String to be split and cleaned
    :return: an array containing every 'word element' containing alpha-numeric values
    """
    # setup
    stringIn = str(stringIn)
    stringIn = re.sub('!', ' !!!! ', stringIn)
    stringIn = re.sub('\?', ' ???? ', stringIn)
    stringIn = re.sub('\*', ' **** ', stringIn)
    #splitting
    lineSplit = stringIn.split()
    triLineSplit = [""]* len(lineSplit)
    #cleaning
    for (counter, word) in enumerate(lineSplit):
        word = word.lower()
        word = re.sub(r'[^\*!?0-9a-z]+', '', word)
        lineSplit[counter] = word
        if counter < len(lineSplit) + 1 and counter >0:
            triLineSplit[counter] = " ".join(lineSplit[counter-2:counter+1])
    lineSplit.extend(triLineSplit)
    lineSplit.extend((lineSplit[-15:-1])*7)

    #remove empty values
    lineSplit = filter(filterParameters, lineSplit)

    return lineSplit

# plotting
############################################
def plot_hist(list, name = "plot"):
    list = list[np.logical_not(np.isnan(list))]
    title_info = time_as_string() + "_" + name + "_hist"
    fig = plt.figure(title_info)
    ax1 = fig.add_subplot(111, title=title_info)

    ax1.hist(list, normed=False, histtype="bar", facecolor='green', bins = 56)

    plt.savefig(title_info)

    plt.show()


def plot_x_y(x_list, y_list, name = "plot"):
    title_info = time_as_string() + "_" + name
    fig = plt.figure(title_info)
    ax1 = fig.add_subplot(111, title=title_info)
    # ax1.title(title_info)

    ax1.fill_between(x_list, 0, y_list, color = "black", facecolor='green', linewidth = 1, label = "lyrics")

    plt.xlabel("Year")
    plt.ylabel("% Lyrics Found")
    plt.ylim(0, 1.1)
    plt.xlim(1955, 2016)
    # ax1.legend()

    plt.savefig(title_info)

    plt.show()

    plt.clf()


# testing - time efficiency
############################################


def timeItStart(printOff = False):
    global START_TIME
    output = sys.stdout
    devnull = open(os.devnull,"w")
    START_TIME = time.localtime()#time.time()
    # print datetime(*START_TIME[:6]), ": Begin Time"
    print time.asctime(START_TIME), ": Begin Time"
    if printOff:
        sys.stdout = STOUT_DEVNULL
    return START_TIME


def timeItEnd( startTimeLocal = None, numIterations=1, printOn = True):

    if numIterations == 0:
        numIterations = 1

    if not startTimeLocal:
        global START_TIME
        startTimeLocal = START_TIME

    #Calculate, print time stamp
    last = time.localtime()
    timePer = (time.mktime(last) - time.mktime(startTimeLocal)) / float(numIterations)
    timeTot = (time.mktime(last) - time.mktime(startTimeLocal))


    sys.stdout = STOUT_DEFAULT
    print time.asctime(last), ": End Time"
    print "  %.4f second(s) per iteration for " % (timePer), numIterations, "iteration(s)"
    print "  %.4f second(s) total" % (timeTot)

    #set output as desired
    if not printOn:
        sys.stdout = STOUT_DEVNULL


#generate_df
############################################

if __name__ == "__main__":
    print "Begin Main"
    print "It is now: ", time_as_string()
    print "\nEnd Main"
