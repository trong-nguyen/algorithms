#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Given an array nums, we call (i, j) an important reverse pair if i < j and nums[i] > 2*nums[j].

You need to return the number of important reverse pairs in the given array.

Example1:

Input: [1,3,2,3,1]
Output: 2
Example2:

Input: [2,4,3,5,1]
Output: 3
Note:
The length of the given array will not exceed 50,000.
All the numbers in the input array are in the range of 32-bit integer.

"""


def merge_sort_count(a, start, end, com):
    """
    Merge sorting the array a while doing an additional task of
    counting the number of pairs that satisfy `com(a,b)` function.

    Dividing and order merging is carried out as in regular merge sort
    This takes O(nlogn) time and O(n) space

    For each recusion call, After the first linear sweep to merge numbers
    Another sweep is taken to count the number of pairs.
    The first sweep is crucial in allowing a linear counting in the second sweep

    a: the array to be counted
    start, end: the considered range of the array
    com: the function to be satisfied on counting
    """

    # Stop conditions
    if start >= end - 1:
        return 0

    # Divide and conquer
    mid = (start + end) / 2

    # The number of pairs in each left or right block
    count = merge_sort_count(a, start, mid, com) + merge_sort_count(a, mid, end, com)

    temp = []

    # First sweep merging
    i0, j0 = start, mid
    i, j = i0, j0
    while i < mid or j < end:
        if i >= mid or (j < end and a[i] > a[j]):
            temp.append(a[j])
            j += 1
        elif j >= end or (i < mid and a[i] <= a[j]):
            temp.append(a[i])
            i += 1
        else:
            break


    # Second sweep counting the pair on both left and right blocks
    inter_count = 0
    ni = mid - start
    i, j = i0, j0
    j_prev = j
    while i < mid and j < end:
        if com(a[i], a[j]):
            di = i - i0
            dj = j - j_prev
            # if a[i] is 2 times larger than this a[j]
            # it is more than 2 times larger than previous a[k] where k < j
            inter_count += (ni - di) * (dj if j > j0 else 1)

            j_prev = j
            j += 1
        else:
            i += 1

    # write out sorted arrays
    a[start:end] = temp

    return count + inter_count


class Solution(object):
    def reversePairs(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        return merge_sort_count(list(nums), 0, len(nums), lambda ai, aj: ai > 2 * aj)

import sys
import random
from utils.templates import fail_string

def test():
    solution = Solution()
    for case, ans in [
        ([[233,2000000001,234,2000000006,235,2000000003,236,2000000007,237,2000000002,2000000005,233,233,233,233,233,2000000004]], 40),
        ([range(20, 25) + range(5)], 5**2),
        ([[-5, -4, -3]], 3),
        ([list(range(50000,0,-1))], 624975000),
        ([[random.randrange(500000) for i in range(50000)]], True),
        ([[-5, -5]], 1),
        ([[1,3,2,3,1]], 2),
        ([[2,4,3,5,1]], 3),
        ([[50000,49999,49998,49997,49996,49995,49994,49993,49992,49991,49990,49989,49988,49987,49986,49985,49984,49983,49982,49981,49980,49979,49978,49977,49976,49975,49974,49973,49972,49971,49970,49969,49968,49967,49966,49965,49964,49963,49962,49961,49960,49959,49958,49957,49956,49955,49954,49953,49952,49951,49950,49949,49948,49947,49946,49945,49944,49943,49942,49941,49940,49939,49938,49937,49936,49935,49934,49933,49932,49931,49930,49929,49928,49927,49926,49925,49924,49923,49922,49921,49920,49919,49918,49917,49916,49915,49914,49913,49912,49911,49910,49909,49908,49907,49906,49905,49904,49903,49902,49901,49900,49899,49898,49897,49896,49895,49894,49893,49892,49891,49890,49889,49888,49887,49886,49885,49884,49883,49882,49881,49880,49879,49878,49877,49876,49875,49874,49873,49872,49871,49870,49869,49868,49867,49866,49865,49864,49863,49862,49861,49860,49859,49858,49857,49856,49855,49854,49853,49852,49851,49850,49849,49848,49847,49846,49845,49844,49843,49842,49841,49840,49839,49838,49837,49836,49835,49834,49833,49832,49831,49830,49829,49828,49827,49826,49825,49824,49823,49822,49821,49820,49819,49818,49817,49816,49815,49814,49813,49812,49811,49810,49809,49808,49807,49806,49805,49804,49803,49802,49801,49800,49799,49798,49797,49796,49795,49794,49793,49792,49791,49790,49789,49788,49787,49786,49785,49784,49783,49782,49781,49780,49779,49778,49777,49776,49775,49774,49773,49772,49771,49770,49769,49768,49767,49766,49765,49764,49763,49762,49761,49760,49759,49758,49757,49756,49755,49754,49753,49752,49751,49750,49749,49748,49747,49746,49745,49744,49743,49742,49741,49740,49739,49738,49737,49736,49735,49734,49733,49732,49731,49730,49729,49728,49727,49726,49725,49724,49723,49722,49721,49720,49719,49718,49717,49716,49715,49714,49713,49712,49711,49710,49709,49708,49707,49706,49705,49704,49703,49702,49701,49700,49699,49698,49697,49696,49695,49694,49693,49692,49691,49690,49689,49688,49687,49686,49685,49684,49683,49682,49681,49680,49679,49678,49677,49676,49675,49674,49673,49672,49671,49670,49669,49668,49667,49666,49665,49664,49663,49662,49661,49660,49659,49658,49657,49656,49655,49654,49653,49652,49651,49650,49649,49648,49647,49646,49645,49644,49643,49642,49641,49640,49639,49638,49637,49636,49635,49634,49633,49632,49631,49630,49629,49628,49627,49626,49625,49624,49623,49622,49621,49620,49619,49618,49617,49616,49615,49614,49613,49612,49611,49610,49609,49608,49607,49606,49605,49604,49603,49602,49601,49600,49599,49598,49597,49596,49595,49594,49593,49592,49591,49590,49589,49588,49587,49586,49585,49584,49583,49582,49581,49580,49579,49578,49577,49576,49575,49574,49573,49572,49571,49570,49569,49568,49567,49566,49565,49564,49563,49562,49561,49560,49559,49558,49557,49556,49555,49554,49553,49552,49551,49550,49549,49548,49547,49546,49545,49544,49543,49542,49541,49540,49539,49538,49537,49536,49535,49534,49533,49532,49531,49530,49529,49528,49527,49526,49525,49524,49523,49522,49521,49520,49519,49518,49517,49516,49515,49514,49513,49512,49511,49510,49509,49508,49507,49506,49505,49504,49503,49502,49501,49500,49499,49498,49497,49496,49495,49494,49493,49492,49491,49490,49489,49488,49487,49486,49485,49484,49483,49482,49481,49480,49479,49478,49477,49476,49475,49474,49473,49472,49471,49470,49469,49468,49467,49466,49465,49464,49463,49462,49461,49460,49459,49458,49457,49456,49455,49454,49453,49452,49451,49450,49449,49448,49447,49446,49445,49444,49443,49442,49441,49440,49439,49438,49437,49436,49435,49434,49433,49432,49431,49430,49429,49428,49427,49426,49425,49424,49423,49422,49421,49420,49419,49418,49417,49416,49415,49414,49413,49412,49411,49410,49409,49408,49407,49406,49405,49404,49403,49402,49401,49400,49399,49398,49397,49396,49395,49394,49393,49392,49391,49390,49389,49388,49387,49386,49385,49384,49383,49382,49381,49380,49379,49378,49377,49376,49375,49374,49373,49372,49371,49370,49369,49368,49367,49366,49365,49364,49363,49362,49361,49360,49359,49358,49357,49356,49355,49354,49353,49352,49351,49350,49349,49348,49347,49346,49345,49344,49343,49342,49341,49340,49339,49338,49337,49336,49335,49334,49333,49332,49331,49330,49329,49328,49327,49326,49325,49324,49323,49322,49321,49320,49319,49318,49317,49316,49315,49314,49313,49312,49311,49310,49309,49308,49307,49306,49305,49304,49303,49302,49301,49300,49299,49298,49297,49296,49295,49294,49293,49292,49291,49290,49289,49288,49287,49286,49285,49284,49283,49282,49281,49280,49279,49278,49277,49276,49275,49274,49273,49272,49271,49270,49269,49268,49267,49266,49265,49264,49263,49262,49261,49260,49259,49258,49257,49256,49255,49254,49253,49252,49251,49250,49249,49248,49247,49246,49245,49244,49243,49242,49241,49240,49239,49238,49237,49236,49235,49234,49233,49232,49231,49230,49229,49228,49227,49226,49225,49224,49223,49222,49221,49220,49219,49218,49217,49216,49215,49214,49213,49212,49211,49210,49209,49208,49207,49206,49205,49204,49203,49202,49201,49200,49199,49198,49197,49196,49195,49194,49193,49192,49191,49190,49189,49188,49187,49186,49185,49184,49183,49182,49181,49180,49179,49178,49177,49176,49175,49174,49173,49172,49171,49170,49169,49168,49167,49166,49165,49164,49163,49162,49161,49160,49159,49158,49157,49156,49155,49154,49153,49152,49151,49150,49149,49148,49147,49146,49145,49144,49143,49142,49141,49140,49139,49138,49137,49136,49135,49134,49133,49132,49131,49130,49129,49128,49127,49126,49125,49124,49123,49122,49121,49120,49119,49118,49117,49116,49115,49114,49113,49112,49111,49110,49109,49108,49107,49106,49105,49104,49103,49102,49101,49100,49099,49098,49097,49096,49095,49094,49093,49092,49091,49090,49089,49088,49087,49086,49085,49084,49083,49082,49081,49080,49079,49078,49077,49076,49075,49074,49073,49072,49071,49070,49069,49068,49067,49066,49065,49064,49063,49062,49061,49060,49059,49058,49057,49056,49055,49054,49053,49052,49051,49050,49049,49048,49047,49046,49045,49044,49043,49042,49041,49040,49039,49038,49037,49036,49035,49034,49033,49032,49031,49030,49029,49028,49027,49026,49025,49024,49023,49022,49021,49020,49019,49018,49017,49016,49015,49014,49013,49012,49011,49010,49009,49008,49007,49006,49005,49004,49003,49002,49001,49000,48999,48998,48997,48996,48995,48994,48993,48992,48991,48990,48989,48988,48987,48986,48985,48984,48983,48982,48981,48980,48979,48978,48977,48976,48975,48974,48973,48972,48971,48970,48969,48968,48967,48966,48965,48964,48963,48962,48961,48960,48959,48958,48957,48956,48955,48954,48953,48952,48951,48950,48949,48948,48947,48946,48945,48944,48943,48942,48941,48940,48939,48938,48937,48936,48935,48934,48933,48932,48931,48930,48929,48928,48927,48926,48925,48924,48923,48922,48921,48920,48919,48918,48917,48916,48915,48914,48913,48912,48911,48910,48909,48908,48907,48906,48905,48904,48903,48902,48901,48900,48899,48898,48897,48896,48895,48894,48893,48892,48891,48890,48889,48888,48887,48886,48885,48884,48883,48882,48881,48880,48879,48878,48877,48876,48875,48874,48873,48872,48871,48870,48869,48868,48867,48866,48865,48864,48863,48862,48861,48860,48859,48858,48857,48856,48855,48854,48853,48852,48851,48850,48849,48848,48847,48846,48845,48844,48843,48842,48841,48840,48839,48838,48837,48836,48835,48834,48833,48832,48831,48830,48829,48828,48827,48826,48825,48824,48823,48822,48821,48820,48819,48818,48817,48816,48815,48814,48813,48812,48811,48810,48809,48808,48807,48806,48805,48804,48803,48802,48801,48800,48799,48798,48797,48796,48795,48794,48793,48792,48791,48790,48789,48788,48787,48786,48785,48784,48783,48782,48781,48780,48779,48778,48777,48776,48775,48774,48773,48772,48771,48770,48769,48768,48767,48766,48765,48764,48763,48762,48761,48760,48759,48758,48757,48756,48755,48754,48753,48752,48751,48750,48749,48748,48747,48746,48745,48744,48743,48742,48741,48740,48739,48738,48737,48736,48735,48734,48733,48732,48731,48730,48729,48728,48727,48726,48725,48724,48723,48722,48721,48720,48719,48718,48717,48716,48715,48714,48713,48712,48711,48710,48709,48708,48707,48706,48705,48704,48703,48702,48701,48700,48699,48698,48697,48696,48695,48694,48693,48692,48691,48690,48689,48688,48687,48686,48685,48684,48683,48682,48681,48680,48679,48678,48677,48676,48675,48674,48673,48672,48671,48670,48669,48668,48667,48666,48665,48664,48663,48662,48661,48660,48659,48658,48657,48656,48655,48654,48653,48652,48651,48650,48649,48648,48647,48646,48645,48644,48643,48642,48641,48640,48639,48638,48637,48636,48635,48634,48633,48632,48631,48630,48629,48628,48627,48626,48625,48624,48623,48622,48621,48620,48619,48618,48617,48616,48615,48614,48613,48612,48611,48610,48609,48608,48607,48606,48605,48604,48603,48602,48601,48600,48599,48598,48597,48596,48595,48594,48593,48592,48591,48590,48589,48588,48587,48586,48585,48584,48583,48582,48581,48580,48579,48578,48577,48576,48575,48574,48573,48572,48571,48570,48569,48568,48567,48566,48565,48564,48563,48562,48561,48560,48559,48558,48557,48556,48555,48554,48553,48552,48551,48550,48549,48548,48547,48546,48545,48544,48543,48542,48541,48540,48539,48538,48537,48536,48535,48534,48533,48532,48531,48530,48529,48528,48527,48526,48525,48524,48523,48522,48521,48520,48519,48518,48517,48516,48515,48514,48513,48512,48511,48510,48509,48508,48507,48506,48505,48504,48503,48502,48501,48500,48499,48498,48497,48496,48495,48494,48493,48492,48491,48490,48489,48488,48487,48486,48485,48484,48483,48482,48481,48480,48479,48478,48477,48476,48475,48474,48473,48472,48471,48470,48469,48468,48467,48466,48465,48464,48463,48462,48461,48460,48459,48458,48457,48456,48455,48454,48453,48452,48451,48450,48449,48448,48447,48446,48445,48444,48443,48442,48441,48440,48439,48438,48437,48436,48435,48434,48433,48432,48431,48430,48429,48428,48427,48426,48425,48424,48423,48422,48421,48420,48419,48418,48417,48416,48415,48414,48413,48412,48411,48410,48409,48408,48407,48406,48405,48404,48403,48402,48401,48400,48399,48398,48397,48396,48395,48394,48393,48392,48391,48390,48389,48388,48387,48386,48385,48384,48383,48382,48381,48380,48379,48378,48377,48376,48375,48374,48373,48372,48371,48370,48369,48368,48367,48366,48365,48364,48363,48362,48361,48360,48359,48358,48357,48356,48355,48354,48353,48352,48351,48350,48349,48348,48347,48346,48345,48344,48343,48342,48341,48340,48339,48338,48337,48336,48335,48334,48333,48332,48331,48330,48329,48328,48327,48326,48325,48324,48323,48322,48321,48320,48319,48318,48317,48316,48315,48314,48313,48312,48311,48310,48309,48308,48307,48306,48305,48304,48303,48302,48301,48300,48299,48298,48297,48296,48295,48294,48293,48292,48291,48290,48289,48288,48287,48286,48285,48284,48283,48282,48281,48280,48279,48278,48277,48276,48275,48274,48273,48272,48271,48270,48269,48268,48267,48266,48265,48264,48263,48262,48261,48260,48259,48258,48257,48256,48255,48254,48253,48252,48251,48250,48249,48248,48247,48246,48245,48244,48243,48242,48241,48240,48239,48238,48237,48236,48235,48234,48233,48232,48231,48230,48229,48228,48227,48226,48225,48224,48223,48222,48221,48220,48219,48218,48217,48216,48215,48214,48213,48212,48211,48210,48209,48208,48207,48206,48205,48204,48203,48202,48201,48200,48199,48198,48197,48196,48195,48194,48193,48192,48191,48190,48189,48188,48187,48186,48185,48184,48183,48182,48181,48180,48179,48178,48177,48176,48175,48174,48173,48172,48171,48170,48169,48168,48167,48166,48165,48164,48163,48162,48161,48160,48159,48158,48157,48156,48155,48154,48153,48152,48151,48150,48149,48148,48147,48146,48145,48144,48143,48142,48141,48140,48139,48138,48137,48136,48135,48134,48133,48132,48131,48130,48129,48128,48127,48126,48125,48124,48123,48122,48121,48120,48119,48118,48117,48116,48115,48114,48113,48112,48111,48110,48109,48108,48107,48106,48105,48104,48103,48102,48101,48100,48099,48098,48097,48096,48095,48094,48093,48092,48091,48090,48089,48088,48087,48086,48085,48084,48083,48082,48081,48080,48079,48078,48077,48076,48075,48074,48073,48072,48071,48070,48069,48068,48067,48066,48065,48064,48063,48062,48061,48060,48059,48058,48057,48056,48055,48054,48053,48052,48051,48050,48049,48048,48047,48046,48045,48044,48043,48042,48041,48040,48039,48038,48037,48036,48035,48034,48033,48032,48031,48030,48029,48028,48027,48026,48025,48024,48023,48022,48021,48020,48019,48018,48017,48016,48015,48014,48013,48012,48011,48010,48009,48008,48007,48006,48005,48004,48003,48002,48001,48000,47999,47998,47997,47996,47995,47994,47993,47992,47991,47990,47989,47988,47987,47986,47985,47984,47983,47982,47981,47980,47979,47978,47977,47976,47975,47974,47973,47972,47971,47970,47969,47968,47967,47966,47965,47964,47963,47962,47961,47960,47959,47958,47957,47956,47955,47954,47953,47952,47951,47950,47949,47948,47947,47946,47945,47944,47943,47942,47941,47940,47939,47938,47937,47936,47935,47934,47933,47932,47931,47930,47929,47928,47927,47926,47925,47924,47923,47922,47921,47920,47919,47918,47917,47916,47915,47914,47913,47912,47911,47910,47909,47908,47907,47906,47905,47904,47903,47902,47901,47900,47899,47898,47897,47896,47895,47894,47893,47892,47891,47890,47889,47888,47887,47886,47885,47884,47883,47882,47881,47880,47879,47878,47877,47876,47875,47874,47873,47872,47871,47870,47869,47868,47867,47866,47865,47864,47863,47862,47861,47860,47859,47858,47857,47856,47855,47854,47853,47852,47851,47850,47849,47848,47847,47846,47845,47844,47843,47842,47841,47840,47839,47838,47837,47836,47835,47834,47833,47832,47831,47830,47829,47828,47827,47826,47825,47824,47823,47822,47821,47820,47819,47818,47817,47816,47815,47814,47813,47812,47811,47810,47809,47808,47807,47806,47805,47804,47803,47802,47801,47800,47799,47798,47797,47796,47795,47794,47793,47792,47791,47790,47789,47788,47787,47786,47785,47784,47783,47782,47781,47780,47779,47778,47777,47776,47775,47774,47773,47772,47771,47770,47769,47768,47767,47766,47765,47764,47763,47762,47761,47760,47759,47758,47757,47756,47755,47754,47753,47752,47751,47750,47749,47748,47747,47746,47745,47744,47743,47742,47741,47740,47739,47738,47737,47736,47735,47734,47733,47732,47731,47730,47729,47728,47727,47726,47725,47724,47723,47722,47721,47720,47719,47718,47717,47716,47715,47714,47713,47712,47711,47710,47709,47708,47707,47706,47705,47704,47703,47702,47701,47700,47699,47698,47697,47696,47695,47694,47693,47692,47691,47690,47689,47688,47687,47686,47685,47684,47683,47682,47681,47680,47679,47678,47677,47676,47675,47674,47673,47672,47671,47670,47669,47668,47667,47666,47665,47664,47663,47662,47661,47660,47659,47658,47657,47656,47655,47654,47653,47652,47651,47650,47649,47648,47647,47646,47645,47644,47643,47642,47641,47640,47639,47638,47637,47636,47635,47634,47633,47632,47631,47630,47629,47628,47627,47626,47625,47624,47623,47622,47621,47620,47619,47618,47617,47616,47615,47614,47613,47612,47611,47610,47609,47608,47607,47606,47605,47604,47603,47602,47601,47600,47599,47598,47597,47596,47595,47594,47593,47592,47591,47590,47589,47588,47587,47586,47585,47584,47583,47582,47581,47580,47579,47578,47577,47576,47575,47574,47573,47572,47571,47570,47569,47568,47567,47566,47565,47564,47563,47562,47561,47560,47559,47558,47557,47556,47555,47554,47553,47552,47551,47550,47549,47548,47547,47546,47545,47544,47543,47542,47541,47540,47539,47538,47537,47536,47535,47534,47533,47532,47531,47530,47529,47528,47527,47526,47525,47524,47523,47522,47521,47520,47519,47518,47517,47516,47515,47514,47513,47512,47511,47510,47509,47508,47507,47506,47505,47504,47503,47502,47501,47500,47499,47498,47497,47496,47495,47494,47493,47492,47491,47490,47489,47488,47487,47486,47485,47484,47483,47482,47481,47480,47479,47478,47477,47476,47475,47474,47473,47472,47471,47470,47469,47468,47467,47466,47465,47464,47463,47462,47461,47460,47459,47458,47457,47456,47455,47454,47453,47452,47451,47450,47449,47448,47447,47446,47445,47444,47443,47442,47441,47440,47439,47438,47437,47436,47435,47434,47433,47432,47431,47430,47429,47428,47427,47426,47425,47424,47423,47422,47421,47420,47419,47418,47417,47416,47415,47414,47413,47412,47411,47410,47409,47408,47407,47406,47405,47404,47403,47402,47401,47400,47399,47398,47397,47396,47395,47394,47393,47392,47391,47390,47389,47388,47387,47386,47385,47384,47383,47382,47381,47380,47379,47378,47377,47376,47375,47374,47373,47372,47371,47370,47369,47368,47367,47366,47365,47364,47363,47362,47361,47360,47359,47358,47357,47356,47355,47354,47353,47352,47351,47350,47349,47348,47347,47346,47345,47344,47343,47342,47341,47340,47339,47338,47337,47336,47335,47334,47333,47332,47331,47330,47329,47328,47327,47326,47325,47324,47323,47322,47321,47320,47319,47318,47317,47316,47315,47314,47313,47312,47311,47310,47309,47308,47307,47306,47305,47304,47303,47302,47301,47300,47299,47298,47297,47296,47295,47294,47293,47292,47291,47290,47289,47288,47287,47286,47285,47284,47283,47282,47281,47280,47279,47278,47277,47276,47275,47274,47273,47272,47271,47270,47269,47268,47267,47266,47265,47264,47263,47262,47261,47260,47259,47258,47257,47256,47255,47254,47253,47252,47251,47250,47249,47248,47247,47246,47245,47244,47243,47242,47241,47240,47239,47238,47237,47236,47235,47234,47233,47232,47231,47230,47229,47228,47227,47226,47225,47224,47223,47222,47221,47220,47219,47218,47217,47216,47215,47214,47213,47212,47211,47210,47209,47208,47207,47206,47205,47204,47203,47202,47201,47200,47199,47198,47197,47196,47195,47194,47193,47192,47191,47190,47189,47188,47187,47186,47185,47184,47183,47182,47181,47180,47179,47178,47177,47176,47175,47174,47173,47172,47171,47170,47169,47168,47167,47166,47165,47164,47163,47162,47161,47160,47159,47158,47157,47156,47155,47154,47153,47152,47151,47150,47149,47148,47147,47146,47145,47144,47143,47142,47141,47140,47139,47138,47137,47136,47135,47134,47133,47132,47131,47130,47129,47128,47127,47126,47125,47124,47123,47122,47121,47120,47119,47118,47117,47116,47115,47114,47113,47112,47111,47110,47109,47108,47107,47106,47105,47104,47103,47102,47101,47100,47099,47098,47097,47096,47095,47094,47093,47092,47091,47090,47089,47088,47087,47086,47085,47084,47083,47082,47081,47080,47079,47078,47077,47076,47075,47074,47073,47072,47071,47070,47069,47068,47067,47066,47065,47064,47063,47062,47061,47060,47059,47058,47057,47056,47055,47054,47053,47052,47051,47050,47049,47048,47047,47046,47045,47044,47043,47042,47041,47040,47039,47038,47037,47036,47035,47034,47033,47032,47031,47030,47029,47028,47027,47026,47025,47024,47023,47022,47021,47020,47019,47018,47017,47016,47015,47014,47013,47012,47011,47010,47009,47008,47007,47006,47005,47004,47003,47002,47001,47000,46999,46998,46997,46996,46995,46994,46993,46992,46991,46990,46989,46988,46987,46986,46985,46984,46983,46982,46981,46980,46979,46978,46977,46976,46975,46974,46973,46972,46971,46970,46969,46968,46967,46966,46965,46964,46963,46962,46961,46960,46959,46958,46957,46956,46955,46954,46953,46952,46951,46950,46949,46948,46947,46946,46945,46944,46943,46942,46941,46940,46939,46938,46937,46936,46935,46934,46933,46932,46931,46930,46929,46928,46927,46926,46925,46924,46923,46922,46921,46920,46919,46918,46917,46916,46915,46914,46913,46912,46911,46910,46909,46908,46907,46906,46905,46904,46903,46902,46901,46900,46899,46898,46897,46896,46895,46894,46893,46892,46891,46890,46889,46888,46887,46886,46885,46884,46883,46882,46881,46880,46879,46878,46877,46876,46875,46874,46873,46872,46871,46870,46869,46868,46867,46866,46865,46864,46863,46862,46861,46860,46859,46858,46857,46856,46855,46854,46853,46852,46851,46850,46849,46848,46847,46846,46845,46844,46843,46842,46841,46840,46839,46838,46837,46836,46835,46834,46833,46832,46831,46830,46829,46828,46827,46826,46825,46824,46823,46822,46821,46820,46819,46818,46817,46816,46815,46814,46813,46812,46811,46810,46809,46808,46807,46806,46805,46804,46803,46802,46801,46800,46799,46798,46797,46796,46795,46794,46793,46792,46791,46790,46789,46788,46787,46786,46785,46784,46783,46782,46781,46780,46779,46778,46777,46776,46775,46774,46773,46772,46771,46770,46769,46768,46767,46766,46765,46764,46763,46762,46761,46760,46759,46758,46757,46756,46755,46754,46753,46752,46751,46750,46749,46748,46747,46746,46745,46744,46743,46742,46741,46740,46739,46738,46737,46736,46735,46734,46733,46732,46731,46730,46729,46728,46727,46726,46725,46724,46723,46722,46721,46720,46719,46718,46717,46716,46715,46714,46713,46712,46711,46710,46709,46708,46707,46706,46705,46704,46703,46702,46701,46700,46699,46698,46697,46696,46695,46694,46693,46692,46691,46690,46689,46688,46687,46686,46685,46684,46683,46682,46681,46680,46679,46678,46677,46676,46675,46674,46673,46672,46671,46670,46669,46668,46667,46666,46665,46664,46663,46662,46661,46660,46659,46658,46657,46656,46655,46654,46653,46652,46651,46650,46649,46648,46647,46646,46645,46644,46643,46642,46641,46640,46639,46638,46637,46636,46635,46634,46633,46632,46631,46630,46629,46628,46627,46626,46625,46624,46623,46622,46621,46620,46619,46618,46617,46616,46615,46614,46613,46612,46611,46610,46609,46608,46607,46606,46605,46604,46603,46602,46601,46600,46599,46598,46597,46596,46595,46594,46593,46592,46591,46590,46589,46588,46587,46586,46585,46584,46583,46582,46581,46580,46579,46578,46577,46576,46575,46574,46573,46572,46571,46570,46569,46568,46567,46566,46565,46564,46563,46562,46561,46560,46559,46558,46557,46556,46555,46554,46553,46552,46551,46550,46549,46548,46547,46546,46545,46544,46543,46542,46541,46540,46539,46538,46537,46536,46535,46534,46533,46532,46531,46530,46529,46528,46527,46526,46525,46524,46523,46522,46521,46520,46519,46518,46517,46516,46515,46514,46513,46512,46511,46510,46509,46508,46507,46506,46505,46504,46503,46502,46501,46500,46499,46498,46497,46496,46495,46494,46493,46492,46491,46490,46489,46488,46487,46486,46485,46484,46483,46482,46481,46480,46479,46478,46477,46476,46475,46474,46473,46472,46471,46470,46469,46468,46467,46466,46465,46464,46463,46462,46461,46460,46459,46458,46457,46456,46455,46454,46453,46452,46451,46450,46449,46448,46447,46446,46445,46444,46443,46442,46441,46440,46439,46438,46437,46436,46435,46434,46433,46432,46431,46430,46429,46428,46427,46426,46425,46424,46423,46422,46421,46420,46419,46418,46417,46416,46415,46414,46413,46412,46411,46410,46409,46408,46407,46406,46405,46404,46403,46402,46401,46400,46399,46398,46397,46396,46395,46394,46393,46392,46391,46390,46389,46388,46387,46386,46385,46384,46383,46382,46381,46380,46379,46378,46377,46376,46375,46374,46373,46372,46371,46370,46369,46368,46367,46366,46365,46364,46363,46362,46361,46360,46359,46358,46357,46356,46355,46354,46353,46352,46351,46350,46349,46348,46347,46346,46345,46344,46343,46342,46341,46340,46339,46338,46337,46336,46335,46334,46333,46332,46331,46330,46329,46328,46327,46326,46325,46324,46323,46322,46321,46320,46319,46318,46317,46316,46315,46314,46313,46312,46311,46310,46309,46308,46307,46306,46305,46304,46303,46302,46301,46300,46299,46298,46297,46296,46295,46294,46293,46292,46291,46290,46289,46288,46287,46286,46285,46284,46283,46282,46281,46280,46279,46278,46277,46276,46275,46274,46273,46272,46271,46270,46269,46268,46267,46266,46265,46264,46263,46262,46261,46260,46259,46258,46257,46256,46255,46254,46253,46252,46251,46250,46249,46248,46247,46246,46245,46244,46243,46242,46241,46240,46239,46238,46237,46236,46235,46234,46233,46232,46231,46230,46229,46228,46227,46226,46225,46224,46223,46222,46221,46220,46219,46218,46217,46216,46215,46214,46213,46212,46211,46210,46209,46208,46207,46206,46205,46204,46203,46202,46201,46200,46199,46198,46197,46196,46195,46194,46193,46192,46191,46190,46189,46188,46187,46186,46185,46184,46183,46182,46181,46180,46179,46178,46177,46176,46175,46174,46173,46172,46171,46170,46169,46168,46167,46166,46165,46164,46163,46162,46161,46160,46159,46158,46157,46156,46155,46154,46153,46152,46151,46150,46149,46148,46147,46146,46145,46144,46143,46142,46141,46140,46139,46138,46137,46136,46135,46134,46133,46132,46131,46130,46129,46128,46127,46126,46125,46124,46123,46122,46121,46120,46119,46118,46117,46116,46115,46114,46113,46112,46111,46110,46109,46108,46107,46106,46105,46104,46103,46102,46101,46100,46099,46098,46097,46096,46095,46094,46093,46092,46091,46090,46089,46088,46087,46086,46085,46084,46083,46082,46081,46080,46079,46078,46077,46076,46075,46074,46073,46072,46071,46070,46069,46068,46067,46066,46065,46064,46063,46062,46061,46060,46059,46058,46057,46056,46055,46054,46053,46052,46051,46050,46049,46048,46047,46046,46045,46044,46043,46042,46041,46040,46039,46038,46037,46036,46035,46034,46033,46032,46031,46030,46029,46028,46027,46026,46025,46024,46023,46022,46021,46020,46019,46018,46017,46016,46015,46014,46013,46012,46011,46010,46009,46008,46007,46006,46005,46004,46003,46002,46001,46000,45999,45998,45997,45996,45995,45994,45993,45992,45991,45990,45989,45988,45987,45986,45985,45984,45983,45982,45981,45980,45979,45978,45977,45976,45975,45974,45973,45972,45971,45970,45969,45968,45967,45966,45965,45964,45963,45962,45961,45960,45959,45958,45957,45956,45955,45954,45953,45952,45951,45950,45949,45948,45947,45946,45945,45944,45943,45942,45941,45940,45939,45938,45937,45936,45935,45934,45933,45932,45931,45930,45929,45928,45927,45926,45925,45924,45923,45922,45921,45920,45919,45918,45917,45916,45915,45914,45913,45912,45911,45910,45909,45908,45907,45906,45905,45904,45903,45902,45901,45900,45899,45898,45897,45896,45895,45894,45893,45892,45891,45890,45889,45888,45887,45886,45885,45884,45883,45882,45881,45880,45879,45878,45877,45876,45875,45874,45873,45872,45871,45870,45869,45868,45867,45866,45865,45864,45863,45862,45861,45860,45859,45858,45857,45856,45855,45854,45853,45852,45851,45850,45849,45848,45847,45846,45845,45844,45843,45842,45841,45840,45839,45838,45837,45836,45835,45834,45833,45832,45831,45830,45829,45828,45827,45826,45825,45824,45823,45822,45821,45820,45819,45818,45817,45816,45815,45814,45813,45812,45811,45810,45809,45808,45807,45806,45805,45804,45803,45802,45801,45800,45799,45798,45797,45796,45795,45794,45793,45792,45791,45790,45789,45788,45787,45786,45785,45784,45783,45782,45781,45780,45779,45778,45777,45776,45775,45774,45773,45772,45771,45770,45769,45768,45767,45766,45765,45764,45763,45762,45761,45760,45759,45758,45757,45756,45755,45754,45753,45752,45751,45750,45749,45748,45747,45746,45745,45744,45743,45742,45741,45740,45739,45738,45737,45736,45735,45734,45733,45732,45731,45730,45729,45728,45727,45726,45725,45724,45723,45722,45721,45720,45719,45718,45717,45716,45715,45714,45713,45712,45711,45710,45709,45708,45707,45706,45705,45704,45703,45702,45701,45700,45699,45698,45697,45696,45695,45694,45693,45692,45691,45690,45689,45688,45687,45686,45685,45684,45683,45682,45681,45680,45679,45678,45677,45676,45675,45674,45673,45672,45671,45670,45669,45668,45667,45666,45665,45664,45663,45662,45661,45660,45659,45658,45657,45656,45655,45654,45653,45652,45651,45650,45649,45648,45647,45646,45645,45644,45643,45642,45641,45640,45639,45638,45637,45636,45635,45634,45633,45632,45631,45630,45629,45628,45627,45626,45625,45624,45623,45622,45621,45620,45619,45618,45617,45616,45615,45614,45613,45612,45611,45610,45609,45608,45607,45606,45605,45604,45603,45602,45601,45600,45599,45598,45597,45596,45595,45594,45593,45592,45591,45590,45589,45588,45587,45586,45585,45584,45583,45582,45581,45580,45579,45578,45577,45576,45575,45574,45573,45572,45571,45570,45569,45568,45567,45566,45565,45564,45563,45562,45561,45560,45559,45558,45557,45556,45555,45554,45553,45552,45551,45550,45549,45548,45547,45546,45545,45544,45543,45]], 4458),
        ([[-185,143,-154,-338,-269,287,214,313,165,-364,-22,-5,9,-212,46,328,-432,-47,317,206,-112,-9,-224,-207,6,198,290,27,408,155,111,-230,-2,-266,84,-224,-317,39,-482,159,35,132,-151,70,-179,104,-156,450,-13,216,190,238,-138,354,171,-398,-36,417,26,-27,-142,478,-362,-91,-262,-11,469,248,-286,-269,-69,-221,-70,26,484,-31,-236,-173,-380,-8,312,-138,-96,23,-7,39,-345,269,156,349,200,52,193,152,168,159,181,272,-259,210,76,194,-31,139,392,-16,-151,50,166,45,9,44,-179,151,-8,75,-277,-18,49,314,-332,449,24,362,88,159,14,-279,232,211,-206,-192,27,238,-339,-79,30,-370,-29,81,251,-189,21,-202,-41,198,51,-6,172,108,26,-168,316,271,-76,-20,-249,-111,47,-86,303,35,127,113,-181,289,-105,-30,-16,-9,95,-144,-422,198,320,7,-227,-161,447,486,-406,-121,-280,-76,285,-453,42,15,-335,-189,-154,280,-206,68,-313,-375,-401,47,184,-320,369,-146,-60,150,378,87,102,138,-54,169,33,-339,-19,147,333,84,92,-57,104,76,-239,99,300,217,-140,153,-344,-103,-6,-37,399,323,-138,279,-259,217,172,-94,-55,29,462,-327,-177,-163,-444,-84,-281,-87,350,-180,20,0,46,331,-15,-244,-370,69,-194,-30,-85,-112,-235,-242,-188,231,123,-233,-29,113,-294,90,64,-3,-364,55,120,-48,-323,99,-76,-70,79,-351,300,-44,-30,25,334,-199,-68,-451,19,57,293,-188,-16,-46,-392,-162,50,-304,23,166,-130,-146,-35,-141,-25,124,-239,114,-104,285,-108,-137,177,-129,-443,341,-112,134,-293,-181,278,203,442,-206,-20,457,-267,171,-321,208,-4,8,-16,-474,-214,-18,-139,-129,-239,-152,45,443,160,-226,338,-384,198,-77,398,296,-405,-156,290,87,-423,-15,-374,127,259,-20,-62,426,-86,-44,184,-207,257,44,-106,-166,260,-181,-282,-68,-90,-39,-3,375,415,20,-207,391,-201,-143,60,242,-192,-74,426,-86,1,74,208,107,-92,114,-37,145,-216,99,319,-298,124,243,73,-127,-139,56,298,24,-354,30,-166,175,82,187,-24,112,-22,-392,-166,-376,470,139,284,-93,162,-160,89,-240,36,-380,-58,-249,104,-1,-172,198,-70,-381,29,20,305,-197,-253,-145,72,98,-375,-152,91,96,-64,170,142,66,398,97,-19,-298,-175,118,-77,-361,354,-29,-47,71,231,-174,-11,-347,-87,36,-318,50,-157,-182,-348,10,96,-241,-82,473,-50,-10,-75,-148,71,20,119,-37,-188,35,65,-346,50,256,-20,-80,-358,419,6,-341,24,-113,-169,108,-488,-334,249,234,-73,-208,19,-264,-89,-41,66,-3,17,-95,2,-143,-11,-348,-324,-366,-183,-148,-76,-197,201,57,-94,-1,0,43,-6,70,-183,71,-304,58,-35,359,103,238,93,331,59,24,-145,92,-34,3,147,-241,-54,-90,1,313,-116,436,162,258,468,-154,-31,111,207,-484,-19,440,201,9,-230,11,-355,246,-78,295,-84,97,43,317,158,-78,183,132,-265,360,-398,-284,-69,212,112,-236,-111,108,266,200,386,-355,36,-3,-3,304,205,-142,-250,8,-45,-35,-165,54,390,175,-44,-255,-207,-64,431,-186,-279,-126,-65,-211,42,246,27,-302,-342,-386,-193,-123,216,71,-391,-343,3,-15,-486,138,142,463,27,-126,-84,39,188,145,402,-260,41,423,6,-86,10,418,-4,-37,-256,-345,-47,49,314,-169,-81,-351,218,-163,0,-6,-432,189,245,-167,92,2,-83,-176,-312,222,108,-18,-119,193,-84,87,-299,220,2,-323,-61,-300,-142,142,223,90,211,107,326,-43,247,43,-27,-114,187,260,-25,-263,-69,-194,-316,-73,230,95,278,-176,37,134,290,-166,-78,135,259,146,-148,1,-210,-209,-59,-92,89,-216,-250,-411,-181,-78,419,21,-370,-9,-154,-24,-306,57,-27,-254,86,-364,71,-99,-70,-79,141,206,-187,227,-362,-293,81,313,-311,-208,-401,-206,-282,-123,86,3,-22,-324,72,-126,-84,216,-411,19,115,-393,-102,-300,275,-376,30,-403,449,465,-243,-168,-7,-43,-23,-219,149,-43,-14,-139,384,-23,15,-10,-263,-375,156,158,-76,27,-263,50,174,305,22,150,-94,-368,-142,61,119,154,-247,-52,-38,-81,-105,402,-21,-148,2,-28,-164,-387,358,216,168,148,200,4,-222,183,281,-428,-13,2,-289,-459,-188,117,193,140,463,-56,159,29,-250,216,143,12,151,48,174,-105,-83,247,324,-204,-181,71,-184,411,-52,-110,-220,168,46,383,-223,-56,24,322,50,-14,-206,-84,-2,-173,219,150,-356,331,-78,-123,468,-184,243,-160,-96,235,-70,214,253,113,313,-80,201,383,125,83,-124,33,223,-48,-55,-175,-364,-98,52,223,45,90,-23,18,141,71,258,-214,-142,-230,159,-319,-440,219,-217,-72,198,56,240,210,76,22,46,-264,159,-153,-189,-212,317,-420,-71,19,-46,64,-37,-15,-397,-27,-236,-135,268,-223,112,392,-300,371,-209,51,109,-465,-219,-155,-138,77,96,-10,33,77,-366,491,22,83,180,-70,-404,-312,-384,251,8,305,-316,157,-318,435,100,274,123,-180,499,-285,221,-135,-199,145,234,12,-13,-164,133,115,-160,315,149,-36,-164,107,-74,300,-34,246,219,-148,-182,26,-143,-321,73,-140,-395,-119,169,38,-148,290,5,319,-126,61,-289,13,86,98,170,-153,-326,-213,152,23,-19,253,154,-116,-3,191,-13,184,283,-71,-116,-315,278,160,173,-151,199,441,-208,-385,95,-338,179,466,37,-50,386,-343,16,162,88,187,-247,328,201,1,-127,274,-152,117,-50,71,59,-33,141,-245,321,-258,-112,82,40,184,310,359,-92,-176,-65,137,-9,-168,79,-66,106,56,3,-176,83,-379,451,64,-101,-65,-403,-193,-31,109,368,-454,119,-340,175,346,-28,275,-293,107,-262,-311,383,140,-7,70,122,-251,-2,-133,9,157,113,349,151,-94,-37,-24,-340,264,-286,92,23,36,-364,331,-419,-107,-342,63,-65,-364,-262,-19,-271,-259,-123,140,-32,29,-38,-401,-491,41,320,-67,-82,399,-294,176,152,-183,173,185,162,100,399,-255,66,194,178,44,-208,-354,-152,-336,-3,-23,-335,22,-71,-244,-246,166,272,227,-350,221,279,66,253,-493,199,-249,81,-189,102,-91,-197,-445,-206,67,-50,-384,-116,-295,-225,22,-350,-364,24,269,-285,34,-123,5,-207,-482,92,-418,25,280,-330,-351,-79,-87,4,-278,251,71,115,214,-141,128,-193,111,145,-215,-116,-216,114,72,-460,142,67,-171,-252,409,27,-173,152,176,-300,-288,11,270,115,-246,-323,192,18,272,-147,61,114,49,155,33,-160,-134,43,206,322,-96,-89,105,-60,181,-78,-249,123,-30,2,-304,166,72,31,145,-131,222,36,-108,142,69,149,16,167,-85,86,-282,311,57,306,-46,-98,28,107,405,-323,-427,116,-29,-156,99,408,-12,120,-57,79,-204,-162,19,-244,82,-221,178,371,139,309,-278,118,102,175,-429,249,82,182,-231,159,180,113,-128,183,-149,18,-126,-34,-319,24,-220,25,-223,24,136,-373,-58,61,-53,-189,402,-104,-42,43,90,69,174,-22,-197,-183,424,-111,42,210,152,-27,122,350,-358,259,283,-222,131,337,28,-259,108,289,-313,-178,-316,-433,-6,-31,-150,285,-56,6,261,5,484,-76,-77,85,178,-279,87,204,77,65,29,-138,-202,-80,48,-407,-285,-204,358,67,-86,75,55,27,217,-183,-225,280,-55,-74,126,279,-67,116,-297,7,-169,201,-147,314,-268,-469,81,-401,-155,47,314,-175,361,-314,-147,331,340,-121,-42,99,164,36,-158,-82,226,-97,-231,48,-83,-132,158,-147,44,-182,191,-320,268,145,-14,89,144,-213,141,346,-266,148,-286,-10,-97,129,17,-9,84,-141,-326,7,-197,321,-447,110,-80,376,367,-122,331,72,-190,-68,124,268,-44,-20,-120,131,168,151,5,8,-86,-72,-335,-255,-408,36,180,-407,169,213,-292,-223,-244,60,-271,-178,143,-274,25,-466,119,127,-470,-323,392,23,-291,-71,-123,-12,-186,-3,-51,-15,380,389,-204,59,-292,26,-4,83,-5,-19,6,-223,-228,259,122,375,60,21,297,212,240,-220,96,8,19,417,-44,-121,-214,-13,-252,-74,-9,-100,-126,198,19,425,-156,73,338,305,465,-9,-329,-79,-380,-167,-93,-151,-65,-299,122,161,-48,-72,-243,-134,-420,-61,228,-106,240,222,40,194,-248,240,-276,-273,-468,-149,-345,295,-433,60,-425,94,-239,-301,0,460,285,-281,40,-207,442,-89,-277,60,335,169,-472,115,39,-467,234,317,-175,192,-41,-438,-101,283,40,139,-178,1,-4,101,81,-178,-75,-204,27,18,-215,-97,-311,413,-230,-38,290,254,-173,-33,355,-145,-30,-89,-123,168,-118,-328,26,-99,-221,-13,69,60,273,475,18,-396,-134,-140,256,-256,-144,-195,141,-334,483,267,154,-234,134,-195,-277,151,-28,-37,339,-190,-208,185,-242,121,188,329,277,-99,-364,-136,-280,-45,-320,160,-32,182,212,42,237,85,-130,140,-233,187,-13,-171,-1,176,-45,-6,192,-350,-8,78,-241,174,121,-376,-127,-16,249,-335,-271,441,-32,-229,-109,80,-164,141,326,-137,-96,452,351,-322,186,458,-78,152,203,149,-493,-15,-154,-85,78,-240,309,181,37,-189,-178,1,-311,198,55,140,105,260,208,82,-281,32,335,-371,-46,129,-116,45,-225,-61,59,249,125,-193,162,10,25,172,-99,-134,-433,-73,141,-253,125,-260,-67,208,-421,-6,-306,473,306,12,-83,-339,-90,-179,-388,349,-166,165,-169,-37,-132,-43,33,375,-443,12,-377,-140,406,-15,26,45,-207,-173,57,-49,290,109,-254,7,86,-100,90,-15,-84,343,85,-184,359,199,345,-194,-246,397,-173,-281,-154,-2,-9,-50,91,-254,37,147,72,-56,93,121,-14,-52,-124,-148,194,-170,-51,-143,95,143,-97,-292,20,161,-121,-397,70,-28,42,41,-180,86,-12,298,304,-63,65,-43,208,-238,-473,259,16,-275,115,62,-103,-161,-383,-88,-53,349,-114,308,13,62,-263,-198,182,-48,-55,417,-17,-29,271,69,-175,120,-190,-154,-263,-138,5,296,-22,-98,-266,-80,-144,374,-236,-220,334,120,-168,-95,144,-291,-137,-116,59,-154,-87,-175,133,-109,-60,278,-209,102,-237,355,-79,230,45,-2,390,107,-152,29,160,73,-482,-234,445,-181,3,-243,-140,-163,48,-28,410,-98,-226,-148,112,236,-26,380,-246,-189,263,-151,422,-269,135,-238,-238,224,-269,112,-336,-322,-167,-61,-123,-267,-219,-86,-11,-164,70,-229,133,294,98,176,157,242,-98,218,311,-381,247,-223,341,-229,43,394,69,-79,-110,-99,-68,61,159,-98,-139,194,-130,275,-61,-182,-31,313,-75,-32,-252,145,-311,412,117,414,325,170,291,353,-105,354,254,-194,-239,-64,203,-93,161,-298,-274,440,33,-10,266,104,-256,-164,-15,-209,346,-194,176,463,365,379,-66,-46,7,90,236,-225,267,-18,403,43,89,299,146,-241,104,-47,80,-245,299,-38,-57,48,431,-194,91,33,210,-407,-152,244,272,117,-451,383,116,-146,-102,-310,-174,30,-275,-101,5,-52,-74,194,-38,17,-320,-138,-23,-86,-85,159,-74,-197,-57,-199,-30,-129,292,-142,-194,-31,-92,478,-225,-371,0,158,113,-294,-391,-207,146,-210,-404,-458,68,-33,-25,-25,355,53,8,129,54,69,84,-21,151,-72,161,-108,62,-103,18,-82,119,-88,-426,70,-355,-260,-315,70,-421,11,-218,-10,139,331,231,116,-233,74,165,-173,-85,12,-285,71,162,-39,116,-232,197,-71,89,-47,135,-340,82,63,79,203,-181,129,-318,-240,108,-76,-40,118,-276,-280,-209,]], 1321809),
    ]:
        nums = case[0]
        # print 'Original {}, set {}'.format(len(nums), len(set(nums)))
        res = solution.reversePairs(nums)
        if ans is True: # if skip
            continue
        else:
            try:
                assert res == ans
            except AssertionError as e:
                status = fail_string(res=res, ans=ans, case=case)
                sys.exit(status)

if __name__ == '__main__':
    test()

    print 'All tests passed'