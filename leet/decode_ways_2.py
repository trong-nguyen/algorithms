#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A message containing letters from A-Z is being encoded to numbers using the following mapping way:

'A' -> 1
'B' -> 2
...
'Z' -> 26
Beyond that, now the encoded string can also contain the character '*', which can be treated as one of the numbers from 1 to 9.

Given the encoded message containing digits and the character '*', return the total number of ways to decode it.

Also, since the answer may be very large, you should return the output mod 109 + 7.

Example 1:
Input: "*"
Output: 9
Explanation: The encoded message can be decoded to the string: "A", "B", "C", "D", "E", "F", "G", "H", "I".
Example 2:
Input: "1*"
Output: 9 + 9 = 18
Note:
The length of the input string will fit in range [1, 105].
The input string will only contain the character '*' and digits '0' - '9'.

SOLUTION:

"""

X_LOOKUP = {
    '0': 0,
    '*': 9,
}
for i in '123456789':
    X_LOOKUP[i] = 1

XY_LOOKUP = {
    '0*': 0,
    '1*': 9,
    '2*': 6,
    '**': 15, # 26 bar sub 10 and 20
}

def init_lookup():
    for i in '123456789':
        X_LOOKUP[i] = 1

    for i in '0123456789':
        XY_LOOKUP['0' + i] = 0
        XY_LOOKUP['1' + i] = 1

    for i in range(27, 100):
        XY_LOOKUP[str(i)] = 0

    for i in '3456789':
        XY_LOOKUP[i + '*'] = 0

    for i in '0123456789':
        if int(i) <= 6:
            XY_LOOKUP['2' + i] = 1
        else:
            XY_LOOKUP['2' + i] = 0

    for i in '0123456789':
        if int(i) <= 6:
            XY_LOOKUP['*' + i] = 2
        else:
            XY_LOOKUP['*' + i] = 1

import json
init_lookup()
print X_LOOKUP, XY_LOOKUP
# print json.dumps(X_LOOKUP, indent=3)
# print json.dumps(XY_LOOKUP, indent=3)

def decode_x(x):
    """
    Single digit decoding
    """

    if x == '0':
        return 0
    if x == '*':
        return 9
    else:
        return 1

def decode_xy(x, y):
    """
    Double digit decoding
    """
    if x == '1':
        if y == '*':
            return 9
        else:
            return 1

    if x == '2':
        if y == '*':
            return 6
        if int(y) <= 6:
            return 1
        else:
            return 0

    if x == '*':
        if y == '*':
            return 24 # 26 bar 10 and 20
        if int(y) <= 6:
            return 2
        else:
            return 1

    else:
        return 0

    return 1

X_LOOKUP = {'*': 9, '1': 1, '0': 0, '3': 1, '2': 1, '5': 1, '4': 1, '7': 1, '6': 1, '9': 1, '8': 1}
XY_LOOKUP = {'24': 1, '25': 1, '26': 1, '27': 0, '20': 1, '21': 1, '22': 1, '23': 1, '28': 0, '29': 0, '2*': 6, '59': 0, '58': 0, '55': 0, '54': 0, '57': 0, '56': 0, '51': 0, '50': 0, '53': 0, '52': 0, '5*': 0, '8*': 0, '88': 0, '89': 0, '82': 0, '83': 0, '80': 0, '81': 0, '86': 0, '87': 0, '84': 0, '85': 0, '02': 0, '03': 0, '00': 0, '01': 0, '06': 0, '07': 0, '04': 0, '05': 0, '08': 0, '09': 0, '0*': 0, '*1': 2, '39': 0, '38': 0, '33': 0, '32': 0, '31': 0, '30': 0, '37': 0, '36': 0, '35': 0, '34': 0, '3*': 0, '**': 15, '6*': 0, '60': 0, '61': 0, '62': 0, '63': 0, '64': 0, '65': 0, '66': 0, '67': 0, '68': 0, '69': 0, '9*': 0, '99': 0, '98': 0, '91': 0, '90': 0, '93': 0, '92': 0, '95': 0, '94': 0, '97': 0, '96': 0, '11': 1, '10': 1, '13': 1, '12': 1, '15': 1, '14': 1, '17': 1, '16': 1, '19': 1, '18': 1, '1*': 9, '48': 0, '49': 0, '46': 0, '47': 0, '44': 0, '45': 0, '42': 0, '43': 0, '40': 0, '41': 0, '4*': 0, '*8': 1, '*9': 1, '*4': 2, '*5': 2, '*6': 2, '*7': 1, '*0': 2, '7*': 0, '*2': 2, '*3': 2, '77': 0, '76': 0, '75': 0, '74': 0, '73': 0, '72': 0, '71': 0, '70': 0, '79': 0, '78': 0}
def _decode(message, i, mem):
    """
    Recursive counting
    """
    if i >= len(message):
        return 1

    if i in mem:
        return mem[i]

    counts = 0
    x = message[i]
    # counts += decode_x(x) * _decode(message, i+1, mem)
    counts += X_LOOKUP[x] * _decode(message, i+1, mem)

    if i < len(message) - 1:
        y = message[i+1]
        # counts += decode_xy(x, y) * _decode(message, i+2, mem)
        counts += XY_LOOKUP[x+y] * _decode(message, i+2, mem)

    mem[i] = counts

    return counts


def decode(message):
    mem = {}
    for i in range(len(message)-1, -1, -1):
        _decode(message, i, mem)
    return mem[0]

class Solution(object):
    def numDecodings(self, s):
        """
        :type s: str
        :rtype: int
        """
        return decode(s) % (10**9 + 7)

import random
import sys
from utils.templates import fail_string

def test():
    solution = Solution()
    for case, ans in [
        (['556653827*4367*734*723*3597794174284617*9574935715**749649479*23244911738*58656921*75*2597574395*98136*1*6*173823***48653296811*33778882864*462143426765*66*8*2754486*2951438*3746977121766375392659*4*85862388381893865*872*216289*523193137359553943997635127831567113774845*88681543638**319119288689927921524411558*4925**69*222678367*24154*7314223286376929*17937*8826554*1365*672989827815152*2697*51*465853582*8*965696*869*6544884311*21*7*2941363663*3826791629429339446297193*371877642553786448666959876427545471294977473*5452677672431364759*483959785*464839543465762676959*811**52541925*7113*662229355893*49844*167534653**1*76*3388181517*22459185959646355953*78538465*173*4637615*471***35*21446644*1852387211142996538351419347988976*72*2229248623643918*973598297224***249265387855993244566*232*2672716929*8267619169977337531*8*8513999*52926591498253938698348**62884969855271511414979246*41*721674959843375359782157366254*41965434113111348413591849*26*16275554758149*235412**42379524125924*6387118224938*59949*9353356654984*2348271*342258122122526*88883176941737*4*419853971*865*427471*52594*785838*6419384763*74*8*61397*779157*4512182*42**46*1*73291495*918213349158248288426*13586322553615134966549***17772291848857*91487*9664*188*4824718724268111669*4*6518**9532544*2*864*1844722973*94*466638817*8*599672*526426*31166*18236132*62353697*379*3787512412*155186872383123675*2733*3*8*992*63688688*8922746693984536*22678*4795673679*3***6381868948563488562*19137*818*488879224*6*538*386*6*23*3852388251*724243946*8437968461*4*419312772*43619776839168**4751417416915645996225*611745568*14*9*1932326628*16589836947*178153392594*46*7*58763859937777*662**278818583659995997796*3725588592*8*56712169215*769427**19335*625*2563347374*551461*93419551887367392**46975687841377244*1876135651894479417*83858947744689765594719341634*53613841891651384352963*4*26618*6*522576827396*157923133426*36239962262652992*9796*552538821784568872*4*1186*989962384435573878391852364*77829684*934276*743415393553599*653*9*1766822324495443658639788*514931*921779*4175762*41176171*13292*9973*72*95*669149*293173866754**6413664144679965*3*96**24741*71*3**5*193767*144799*959573*425728622815417991735214**599215395688282741*61856*18545462711*82429721691*8*78833259214878724*922818487871635269219673714145129713588*4479939989241689614*6523**3347747975*3**3157575374658153772*9859389549271192199797279*1356562645787*443694639123373*654**95*44229189*9*38768695*47381845843879*551936**5163394*286551696135672*3163752182*223616966*683*9918123*192958*7192836555991819459612137526168547424848786*1292*119919619*14*51613834693269427617*8977856843223636*8826*597*8841514336653747871486272828497373592492*934499641231528*71741*3*789*89569575817856124*12667*2*427688867315161745*37739575*74466662*27721*82871299982639446276214*38278611329152517*261*85242*6957*8*1725*87447797388417393476764882*15718689559538168539959414146919152*962383917576367493465321523*54227*7397322781953818*2624265469337895215631*8991846318*252***4594436943*227496964182372287*477953252153286777745449358*45747*827553323833687657*856**929584178213747*886*6278778*952217742313993846335139217653841243911*1438682231*41364979*839396695445358345863688*397941267253715833*864*7*96*49319291745*5187**14262373217827**5198*86776548544*3*5888126785439498331686694*674433*7398316*45*116*1*687*948494212189*65745794917431679285381533*631294682898194728*47794**488679*6384688283*85*762*64764*69837949526172886892**5891761426*32*8669646745455283*7866592152826111987*351649545654287659*13635293638*1*1672141734585*3296*577*97*6582284141616493649662619*2119*1767292575844761**53647795493*9665315423*12976239922895962757754586186*5*8682*26925*38761676177788*553*5*992*8*262791916544383***952*786275*5161451973*32685858467333362497543179443541728981881811*5*79667114274995973*39862742814*5392656*6832*197*7139646*9485124498591215*91666*1798147638918132549*539915995246755379*362268464326875193*43*225*98117*261299227942128*4371691411842*11897523*41392*781785132625*52424418*42851277175747313774473461814*6*828*25331*76861962844328885*635142216561545*57781987*45182712538532635794563138642881264756*127*9643478*39552497717*729*332248281585*32144*9*695*73*4439772*4874*58*5*89*4*81*423364446739*9121987861886348179184274492592542631925531395*1858595995485649***47*2494872171312592985914885649137794*1*252172*337423*699835*5521215*1982888632429826467*339273356439956*53368657*134299229758227*847475*394559885156*12214816398679968649313236234231645228*3654858253584877323613***74*3572167322179*1693*2999492731*27887*783*3338562*54219**3165681855*95886792339679**586137591953***79*4685*96435561885319*8*47158178567359346295*14169648472448283191782154141*4*5*9348*5*2271312368985**921256*515517383*4666*316556*2847928*93434646*514196545614745*665561898*254*4365111*8345125546913928539259939671937887463*5755884948438*38*79*2914897364*78737962184*946516*86277291622*776688348542635**6285854521*8*6492535*75167524*7142554674**16872933*59*387*817845465569268283774252125813461578478934759*62423191918932119251954*11129352348315**446242154182137253*9*65768332651828741333836817*5962932256436424759587*4236823914938938945911542966687*5*814286*978262753161345228342858829*9146114756*9439564187*7999*7838316236999826692642*984174*387589*7*6879**7992798314685*22733356247559125852458719742241*124623386549768***6*137434561*52542733141719141*56626*239494928756988793446*891275698*691121*6*66266268*8214297978319238588*****7167*5563*8321*3322*425985351874*3*1738888669149*942*859749567292583549198648981397**69817373472*427*112886389*67*44416728*21727*86876674484839243743*945*75354853826449345335*48278*5*122979*3841432*3915338217*4*653*4794924526887532586569656*916659724*3158745862117355649883613*7*1224*233765*2964732555725*796*897744642527*1382159731581657*39845287368198821752229616762346698*613169693381452799138167358257471373643469652276*8539198979869683312495787775*6*344573892813934*2416*51*2635*6934*37*5*551*6*2869831714*5449*3378616196489487315461547332813*72761957727987554411411459463335934829*78681773859**23*34535566339382683758*582684*4847847*137742556173*5*336575447291647578895*9*238*236893597*615491974424675222366524*347759634835892776828183627582552299149584236173319278546433931836793934458467544822*871573***1769657787*3623589566*673656457*124867*1271747224184622915*481248767745861*468333*3354*576296472943838346**56*262846432883882212324912921*225532388323727433514*821*8923*9652536*323*3793**29364951876225581555**7533*776478591881684872*744633*81754175*231236463551623487*794192285636797512884115*32*454716911995836341*35883532712383438676815*469161442421*22828191697*7943972843238288*76*17*4228354213815186*3897479416279954592649*316**112*4924811963437*73334965661*238538929*3414968*43438294*1964894*7747*139931319131*2*439346*865839876*12*3697546*949918*339831378319*376922157*22658768768735213557251389147*621951*77419759957193799*9*1*23348193423468**89*787931195591478*1422355536823261244*2386323267*799*115*89273626466299*298412975954117767423599*8*3*8936911*44838661*39465173888626*24162**3873972582*546*31926814785*41443173942914251237*5852353882*9828726125458868857172885556682813349252199326263226124*43123778**3239656382795143381356726673*15*77*79372**7*841587371338282*978226298736549593397782725*56573571588843969*7*5689637996352*68*359778*8996*5992874167*319715253732*943*93593*2498*3124764984839686436*399846163475933411691834428337627327633*828596581735*791*5123271956788564586*8827398815**46*23359**444*8*16249998221319721745*696372525*183512145221267351373126944963*1491*12334754587*67828*22938*26153991711819537*25*2***95256453394385789763848324*11*466144677542941735249938646299523**277*184236482*646154261937777*453683159996**28937779249519611365419948618317549432564*32*876*9588382292176826961379*334*326642913*6828489*32*77413514*191*8412571486433678859377592*62984*34*87757584*588*79376199615955*9873*31818675143765358157551437643*78881757982365373317*3364596376193395*74127*7617*9*452*8331372784415379158991251913515848628569845531184624617523246398296993768742166425961118999274657*747*4124232337763514*91475287244*1**8739275467*874881*863815955349329271145978763925428252249534797784*865256284*87634817574651*73194267884*9526*5894316*831194154**1*237243998159324897812**349889582*58*26964871175285672576957143373745222295162275672117174795*6998544*9843187*844959*22*11177879744251*8537247453529947853421945942281845384527773*3247478*2411*934968*312344*25*12842*329657214885619687671*47*1611*423289233664*47671388133974*2682248698293542766844871128*47488*9193414518328659*139*4142623477559762*984*8*26616334118244368148*367*8692*79638225*4*93*627482641643754843*8*197*78374343715179*48*696735867517499*749639989*4*4984382143195*6152*591291646*281751773524464*39628321*5*7113*85626446**2366944259**426796*182*4881*58449221434974686272876171116*8727641334336688233778676*9565512151*934246163755378*35431455693699951229898*24125886151446*4959967678*53786965352*78*19**48821*17**2871453882314825645*9762618151*734174*3*65214**21946456618636712998897*62339532652941777899856461623*3669*157834*2656271463*57558971469613187*63169*5788389479777175*519*4489*2725*6289*262626889437414494117355899398654*27534757*614198299*994777531452693889179*73678*61228781416432761134547326295*542425581241753727*9935864183737922535712**88613*6445*44663871*2419577659439782*27437*33733519*783*992166126745962*776*4633819878437661617*95961612516558535161*356434*85791737148728*44764944945*1*534*86*2597115929852*51597359869163838346764152131748947481729351821958737*69926417679978*2224821352799359*4*1*969328144663523**566361969529952466226*2317*9539116658457*83*186*886872258*857882***761*1137557247971787483*5918**516419386**77824686273331254773895772*9535437259338784*26**113351*831542661373*94727666565413336866*8343261643274187319673844*1498996641*79859424589*28983824224*2*284438*377775261462643488943148961352597564846345251249**4571825*6194*2178911*824698*491236*52*6343581*6429877596577*5519588911*86743868788722154954311727477347255681132717196628245*8438854973356153262735317*4475*93***867*22*2839568632142*47957281172611287291*7**66*17767646*1628*228444731*77294645975327429472362576657562665976899*6832826*91355169213**95*7584*43*6*679536575461313**997294*51164797*45151958898351582311554*2425*19136545251358645652*292313*39887254222131696988223666*4384359372*6199997*322116574839*818344736592989965715725493*1*3188**142*28629872576946165745619939*2*68476228348821142391865749249534841895*2473*53493554*835824156*727297349387*1953111518836*672984765256614397*4584116289792814118*466413*38*2928782*669534527473847117216269935*936444366183215124225971859*3556*942593*56946694*926*862426853935658*2538911366655774*67521*6791843457119978944452898*33*591*1**45*859884674633647*682*52598*154*5886822489265311886178323838****751798887*4273*2281823561529426395*6458334*5368464493654*39711255*59423696*964132832639296613*5273118347*32266268975596815961422792*91141*724948983153*738*83658858558811923565221*64983*4291*647166*68732731666543198*55155884782821649469**8*46967*94*9997362*433127792755379353*8697547157488214847326883849485119***546464117482**717*7423*777624587347714*94*5959*6483214759485448189*6818718*3875*974197*75*73*9925751665*59*46699*3231951257*424757667*3788635228435392377129*6**55559**545475327**3262*8*5375977519781*664999247*256363347883529175*78225514*63*4544**65765531281389782993635239859721*954*945331591*7826984628918281426862816971861*797367542*78593*175529776*41169*473*4854*4*6771*5197*4*3313484936534722729475498142871*37298422**583*373464856*981825839*7672945*28128947732*264933315488157616867886892872167369*511542496294*1635793*6*68*1687658729253288*475**7186963*33461143288612451472*1251*9858469881482548*98239*243752*91522*424727*626*465113*44869112*516*8*935*1521293*51*99828*627*7*2225*4529*58573888191464849*746392597858392*7556*4649871711214685675115993366*74962231225*9*97*7719627762736293179294*48598*1*635255*98828153775416*51*349224*66946835982341*2*19371**496811714467676*38688*5112*32*527855*442174715*3768249863637*17469168143*814*9*621*1982232989176691416979*38755515413*243*31171819*811923326*91522285845*856814476*38644499*488421351755*2243*65662689983*211798*27*7*4397444896365197559495*16*2298553593394485*978672829141539475951629*9496931316272554631*6541374143321428194855427*456143547711181134492121*1655836688651927166859392*4*4146913339*943491341738116391698428**2*3758613692949*22227293219589*214457916*4651*84*124*8*18415417652258*983211314*46149693*5568938111596633831533*3981*6143776925215268328*7612718114685678*7763184*6321575323**764247*9874891931479653851**5734415**91682943*4249132949137926379458185597*3467912*62491341488318796365*95333772397683934921*3*8*14546431*188851638654744233879*1831127839839432675533145791928*21991*7126134823*262728*4142842977*11432947785371348471263712*35233589752*387482*93*18233773631629335148*8684547212268779*981153568*5941329517*618214917742111727829999441*121*34842*12564*93715473875854562196313*25999*7876*5616798*761935941656882558374346699858477484935539*39741868*118141**316524919211511381884329775*5132651399*613*753595*6*48***38*19266964*9*94393812528353517919349*19956387444**795756*4387496539671*834666*8928533633818669454544*32694436*515472**89347633223558862122**2289*163297223534*4458353325852551859468**86634728*531569842851231*4157222*59734633439713*97453554412377147163149753173581*7699765424128*842*97174*444154431168*21*2762631919691936483**56787289*656522*17*632884545842738953122636485123*5**2846*623421775224329217193*579935776*949867551*9469616918*274424362595112*78847661546*2*2176538*286252262577928*858565**2346579854368*8*597*76*449299**14478*96394*3568856444693311576869596*95358584337151*2*13347**78951313*1615243544699493128285*8557175675519*442319*35*9134*652634*66386315522629338464237922642*5729692*834288*13611945747482616386567257779591*1*7769*29*3113**646**71833226*3349*6913111324216264*12458858497*92*878347*1468*162*51911793*1112559769*268166891398954327*5*4838574559688*544489696274137*8771716217*89955328415891218727913324*478764984*5148*662*2*9**82713913461936332595357442941655**23*55738*63421735*19*44728964723847226392*31537468*5529855169269597969414377644*46447*66353422*6*931833942585*688995376338765641295997258891922346948556324837349378133*89582*953614868897588*83*426282**91*5734*288*2*5***42685*76*317721949558*28858883*19689728984****2485*9128744644725287811916839865532893*41645*234756*1779762782*66141758426*842637927*72668**1982359799638753*971156889*7*887*468568557523719694413699*3614*6682682944359*51675767692*847*143379985969123**4388792522798*8881753287452516853155897148*29*272*987*5224789878758141788171382333*4991676423918*3*818684558**2171785168444*589753676672416375566416626376495159284113175829331*919652*852492664269*788*791256153652918*8275161821**9328*3678217*164*812232426491285685**1*68587518494*29245*1*9924539584347*88*8675*68358695*3749*37176196*929833*7917992*687415299863667295134732*3598191885*754147324*49473*56**517463*7*242699195*9*1*68733311829635525192629762228654*8679878938257111356243438*7235295527*3687*43*6526*36*315311*818179278*75*342425*372*25976**738*7*4595619**714*36387515*842931735891725462959667*14*518*81*275649736275299792686*631656*1189499859*24*63411588*34*691512862881469*7**2*276916631485961891741419981912558891443848198235572333819*1772414981*35883524821114624*691897*716326164*624232795*48998358*722836698**5545329542456931499976661851*54232167412628943622111*7793568289397*7943424278*99755667984754989454512363*1677971**24844275***727*8468637766142765*558694577*1284399378845*4*47*2*39638987922728*37*24592626714525*425*7581144**24375137493435528464*75*6479832677889753446864526938233331271*37931*273878*716246*523877914*93598764493862294563984*71682168218494273894235573654294996488675615*8864848229352683732481564912199446379378728776*824*3662716312169359388118*211*941683152722748453*3699289449674443998223*19779*641688*6615*741589*6*684*332992*7126828385159662*78**6*4915311*823377459327632**32154385461632**12383722526894272618851795959*44*7*12834761888266756132*15428388649214812**39514898547226*61993*495245192912*487*58378886552*842138579224346594*43972842544*84584863752333*38677*12471*9765915557641772221789974*275*242445222693233*546339627883*542386743566*477538**76*867567362952793*671839331*965*84118835782*9523175263*927414991*193*398981*7189*6975766336972552*5454639*976545732464646959*8786653184953993755*7237849174479986994919888222*9253617716637*2842985265**352446*133*15777415165*9873329*636578411*1*31546937*39965388541*787876853*1914127146229761368568717836499189*72*2*529*199*49*8525496168436114125156*61*335438174343142*4439463373898765841756666759447*67*823565*56*6*644*87*2157***7881*4177397587*7588*72484*25822937767574165466341211564979662627422**1885593218639*16951937*2823199*1245285966632265242*79761377657*969751463887*422594**217641349*249229728535824*38784*938*147*45*665*1229114153**262495*127547794*93*72*1*769*88725*38169441919248293131885633349*9243643347174149791112835856*7816728*1135556562**8*933*713891794*198362*915216866655324*7394*67774789252246*58571853*1532*221322689*9*7378319199974**9454663846*95514516722461*29*54787**1271271872661*2162996*25*862974*872521812247681879*785*5654111218725458*81198659922828513465*134961*35221555625*2886785*715*3346267373*34146429*2748575883295293*948141*29782314629*1*7249453**17624258675449*6*6872334914696681649468929*2895*4689*6536399234832386*571*85245*276193786571*797351*25738826343*6317*213*51222732729423741363*92892**685*89342*7*9963*18395166569987171982495567*3544*3762**21**477159299*354695664259364459633*245578785374342691331493397788968**5641252971661*2987995988554385*26919641695255143*361377281674534539269957*7425*175949919*35559524*91**91586919734*663368154668645763*6*9315232539864*21824*529129*816213525889252*1735*7321153189*3*286*78146229369*72272177241*45*33646867*12776*278561*3128364*665157385*99572587922585253849**95*446652571169841229*6563983*21197*1899*1925636*614323287263*528921178581237*76*79835567*5417*4394749956*4263614541584191*814252736*6278*213741*31734342*2*62767*2*8581458*664458*18*36656623*9*43*91548399996*88*67956***55*61216963188717189*5*7*5698524291**84846946545956*532688326939572143718572437*652879557676448*74743*396*564935232869*3**81514148*16535828129371419*5842129442527*8418832583769981171465934156521461932366318*859463883*75*9483682*3393145*1*8*17874373485885564979178*8478269266*936871585262443244238795294347**42932*916872559719617811542671226*6859**626795*6*8**48875**9274175**67166495765331195275453677539623886382538*874367964881684*78618626623531*915394*3372197515*7914*2*94*49*4*7*16417487773921336282656798239315*633*882*79691635294*46936712189278298258672*6189*71695397578865891*3638573934571825718*5358942318964*9122679545771166921226323945336648714895896618176746875698133*83876*928362*95319495*32554755456123927439*664358581475658689269415995*644899*71431775658126*7627483911*97979746379*247*9351717*8583**9156584*54*2*87*797596166566454945455*22*3812*66317831712*9845124*31696*924**8279661564153251*5*715536965*62278*8159**5695*78*2765292892156292627*654*88*33548*2479694733416725795*931341655714425523835174*24*4*2686472246323987*5*76491984274429*959954659***74289992152171*87199*4**1161522859291897*2112482699421617*5424*547363*397*496*9837297864*228*9697584*657*535*83*6687*9343464*634797975422*81238*671692181**275498698*1142665*6729812272671349622289456675315*3*13264*5745878*1*51*87*134**45912493*16226*2586961532**1667653497686254878253853162874554488497472414797329437453885547968744344*986615947157*25*447*23328129777819*461*9215144436*842*122991659962678742*293544*7512718487*8965*8*4657**9187439*23*31766*76552192*7*123*791343*421923876296265197317846313659621489142243936492*34537792*963344448945788322729*2*66325*3368956**7941858582949*17481533416852237934*1368*358488583*89426916796437696397247918289764491**1613562579583498*5*7487*77596513522*7124*36228583355491*6216*88512428848*9**27364794413361189*4562229472*21658751214*181*586586843725*6971228193*2162*57778**47862*594975*433*1*7654679541643979232215*64253713943841311198146276*34437493784542538435*3*14682*351*8*6*433436556463496861969295345*9679*82337547599**57449672752369*86695673212459488637691996594565557*88*1*33638375*793746966865*35532*8831879**9*27*81**76*9929542314*3212315*9878**5923*91629667**139421571172835*63636*5321996916845997**51112487728179352*548*72***82**6**492961*2**4223837198894294568318397474272822*6*462658759143485537*43326329244*3191163586194*7597769*47154985976219925*198352*9343528847*63315744*555629**9281394874464*414*78*3861394527919731219663*266536649336*418313*5*77*2388668969914299*3421747717824*993163*36251**1349467*933*22539962*35*89166582524839*323694*5*877565445347885555596*572431238647264**196382*5247749737265*1944*78248*784125*262868499817*95795*292*17343938988*58882*6378**916*5384265822212157*1*2197879641198587314319261526*7821*2628196774757349*2283*694179*6526779324943588*4593*239457*284779994964969*4212*937789843328843338443553*34*61*443**27924372597372*618**52158518757864773863683625465219136156*7125868986279778142575*9884329687145*18488713957584**16743*2313858546727645231755*94871417362941919546772839189285157*63378158231344852969125915223947*7493*2*88*8715662*1379612911861*7113*4173643628263534238356*99295589857374**8*68*33648*6717583246767276645*4324397238278917425**759**1932264785244**597*83948453*29818271*1167*67964654667689*4181*573*879441754866224971563639389699621*84583561881*942283*27*851*417*2194183916351765*77827882*4*1495272*51458**293613482955771*17**67354*493246718396194439855681358722575371594694*566167348*986564**183284721612844365596*778491*9993876*268537999699*347932*95239942*86746174865115499274944634941981249532561965*6395383924*62122736639*7849233532174838*7*1832352467937539**297124629766671284397228*3925*9194*97915479313146435994336169*7**387426827*6789*9*961667524*9*7467234288488715879829*553*2*166392291951619797*5**6733*28517857*3959663499*374284*39963**7253*3623*18144569197*6795516*9*3147*93123768*24*32482435685*87*54894185*8*9*1*79*8749989518*371*535765491*54*85372575644522746*4664896469462286*2*383*92724111*7*824971886476961848951562115*2452428364**6991899*691549*944878858996464817*32891922711467474987871686486229359673775812339492457*5366527*4157*13627773674*995195796263*46712613*2372927*7997*932*17818569944294*69595522895435538*8197598**8*4898*82*56549977282*84516222733982322*8953*6226*8991947*421*81135584671269529*58716439841*314*31*339386*9*23*8*7845845154851*4987175574339717*7259489133245984*6569*654861*33193311912324912165*29*5576*2389518*9253263**82118991785*8194*5545429683213*117671736857213776688*9228994154329*22561**9695194886*46824934828647873834*143*87*156*8217114676698776*4888771641**373463889546767257552596159631*6238834857978375374*994818598*65525*77*7169858*483662649*53*442489711165784499285674771393*147243379*42*556968769474673*843*387736181876793467196384464181*24652517545411*2825811627*84*2613678112343185*65355*1*492387*48354473647625585843526111915116638832598117783698155811894964624927648**86147335*115337*86*3812724531394777556477786668956*49*66523*12938579639822958347*163495686918985*9775266266*834226795411474*84*843212334*58281479995424296693252826394157195*3821*8135238759411575375729**323643124988*51158479647648589829412398826379784*2*9*727599818157279318823578*5222622883*73532435936*1411547711126834267282*2248*34594421654676612928846984*865671*1471*2886637*326337*69*71352467552414971675733649386*15116814378878616931*27241341999*4512*779*3191273*835861522858698*8377*5*65491442**41634*3774146393537935392*39*9646822286589863864*61583*95531*2**196144723*4238123*35843*975*558219*51662*31454549554*53288484215841132335678856*8*743*98374332999*3723235243**93*494*3654*511833694987377*334*2171222*1546698181917328872333213*53388*5**21184965*4568714996918562871*589*4145932271614375786*21462123489*8**214677432598167593*4*666751544*5366653862*3672271921*146*3811**358436888427*8*48246*286212952419926*576*66611846443383*1221*738865424748*3*59292769965*3681472393287*18525*8373*55*6888**642**1777136397*477316946*4637849584*196747583769221432*439537755835159*392958286412917979427931868766761667*689958*6993*352956*52553323271*36564717558*2843995*5831428851721728*597943382*75254741*25439*551787**723**5281*75398344524*81*5727581874457*1481753*8836428525*79813*7657515867932566992998462529*243414*66*5725987223795455211*1*97893531*8128829*92*2*4584437114691746*187629*9591352239663663831667127*3*2421812243668*1955166*475*6774*5*94337*22983*798462*352417531598316*383*523885393*1359375171867*16471*489783*4718665*79661827216974*533382*8*8*238*23541634*7*9*67*9*195*3623173315136293262385778656617**8476661*7837775883895258674847224*93753623428672152465*75412856*4334341186*985394*89481725954452948745*42*489*59379*815761417*36*815*81736882252141859548984225524622354138124222*691765412*12369**51*58863556282812682677185285*626617*1543411555388*33*976999335636822935827178314*428*53438755979*2295*1614186*3*33374358388*5*823984*947563*7*933*8892761936972495*72946315539995*769719381643184*21158949566456279742548359*637231731385*178*4486626689735988514276698*9315182132*256627**1547458*834946457973538269152315185684*145822*5772247963629**2917*19612933319655541775579943431931181917693265315584*89494976767*542385*1*254789479*2644832*2*78468818751*2*2*34*5383878397149311926884395935*83*42*88568969322866721*7134381364296951485*131441345512938*359145415*6361465*521389678246*433*239765826911222637728796*594786555221496376545654*23*24351*7*55*4*698957333738713525413343227*736*8538371684854*134847268941826*4362*3*2329518641142**6316738337*7*2532847178788846218141821161*98889284132233274658*5849343766*45*1*68*222529432365*768116535441274442554*5433859251649*451*4*5157*17967993**3939413516486749445*74717265*23355334913732686*1632313893642324573442178847*7*6*386463263247544*5313*757442722997*69162435325818265384252853299786898931419192896229*3*8*86565*4*1435997269745255844252**749459573*35211368946473*257687347*225128*5543267*7516342*469439259718658411982552663759889*7651*11559645*92892*7*753768333182721838*788857*34**541418693867334*6498532*547*7*771549696171882246186746*1727*757*53*91*1692872772882897**747476961414228499894856372572532111296339*181652414*258861886567*554535*449779158254361*2548611523964366222**15*4842277493458857*2*332*325969255*73857*21616179831*37874221*37147632186288151642548844*76*25768429284599321*4*54263*93731659*44154*2499*85481**19322597857799719349744*547229188791258*4187317688144269847132*3888832883*34117336494*19482619129518736365737218835255*3*9*33968447297*399348*13298524*16*7*8574*78*295523769*743575479671659*2395799873*6477*14*5*78597992*2379786113651219*661598171826639466821511469387849936887138724278613*8442123884869671*584448*4668371793179388296329553776365*138957351782451*8221*2893151981896235*4242365793*835753279641*43471*4294*1*3*9*43*663*7*1*92956514389121444748*164256578*7253832735**79688917925768224678284*564*28*7273522132196**2291613879566874652946657448612937773*24593*761881791735*7724476*5996578521722514399*2462**5525763838863332*5568573*484*2728*3138546541*255899*29893*4118521*456**16752*356*1516687713*9747764345615748465147837718187753536*36787541516*12817279*148558*33292492599662525533*9665561*78875643*5632849228342658924828531787949826692519*7271354186847362*7327783895751718679862253778728682*93571471942942*6584768342118*88117*71493787731158*5229538243*62*16*984636567645161*59132597*15227*7876563*5411684691998168838849693*26481625614817545721131251953*293473845755166159444777*8923*93**172**389947*53591447*5924689873369523*12497**55941331*99744547466174122784484*389*48*2*36771762273271783*3884*3*538751782198853597988129*4*289529619527831644418*428222529416482928*4514357454726356584855735686287483813848371717567295*818259635126833*6254*7389276217851*5789491*2178*872*11677*468*739***939*64523827**836548625516**84162373577*93792529***45192934379*5*875*2717*67337266*583172528655524557294384641493289912479732527551313322*94617549*57567568384147*17849195*8379493734199432267385827*67*3*3972*476319125432435392987938667748*8482*29928727272*877633136871*3*84975524379*8235**91626457*55347229885*86275*4975393*811*6853119747885725*91612*29*68478555418625*98712119552227273*149*153595671392177812338248**187392766924778351***394327*9*792191279539678366858676*856*91438724314794552*774782915467*8626*65*334242831944669897227763348424634211168596387945*298**432985*6924*781753112512731562566729*5*42857*992782956**7997286*16437449***8*97*4167*698264555823284566*728*983551532**645431977*35977751876155847*346389966795893*8156**9*1181817649576955673969115276452698142865*4218932127*4965931864*777731**7745*4839172*15*2*385339384271*4961116*4169516471923**84787549965493154531392833752286838797767331323*86337*37*189473898*287*7178*21917633645443192414219163*88**9917398*24752321*64534532989238711633485*62952381549544236244*5212281435337974614618573526534397729557339229955*9879287159137935*56799*31871794*875488249471581781194223116735138861362955228*27762614779544971229185175*387686933738251961611568*51*666444819449116355*547496*516*459*48585534488*861354866929*9784428289184643**886373678466638869****291219*6*21965733236245**47*4485152*121931869712289*285338*938478396958125292*9451779*35743533586385136657*231692565412167129232*645724634652422351582848*469454623*8365265845722572266976317279438472447937*4745578*539*646*753753853238947*39993289429562538986218579*1427582199*724922663935234768*543**1994361324*869748332728*591*99745473793444375113615*648722531*38*9728*61881113*1*47589*914743*171526*968871518*7911318875717993*1476667511677468*798*18164128818568839452232*95*52854251*2*963**89**11979866315722162*53*6*612448798566*96864661675744936831769123948786*89362151*27387426918213195862*27543268472*34*27*1*4224367819582713479179675668283132964569699522622939385387286383388792183585617*672911399*7916693837877*44*41877*4131587*89967113175*7414977794232753271411911*6519468774*9*24245656498763899123*57*1485445*661872219562553665687767412346*341841166284938463128124379*61423*747715665**8*4293877919163519852123621751332774444568135*233*15247*5*4**255878389794446731212366886459428*541*57642*93242284**122274895256*2*23642514*964*181*67*195*7362517293*651524*495923559*797719*6847*338195743447543*4992136553676585*519331633*464228532836*473556737**976133448643417564556812218337692493*18713769*95262*81176955399459811*246*6323*586728272459354*24348964772781*1953919976165958297146536987771787965118366899638*77258281*6*39464876*22*9327*93956**644271253375166868*8169492356237257595343*29*2528957*13*2786237988*35269*1438938228*91*54975*498*28*2152*42234816167*1269189415*45485835197214471179232264*1717831*495*3315471192525229189615763988673287371118*297276*1945*13873258985*595*1337198998658955277*2*38355915872913378*742*946612567*66*3*15592918955817391125*76587531*9433954438111292*81169832**875611752448*38726661482911166111847*8*72613323599212311*682466265862**4354349714933*66115*533384953*38318663247571935284126721452*6137676867328712**9147119*18*8952411*5727*3*581789247845968*5152925191136592463661779279*46*42145556159565292182468293672211*772*7*14611*1*39276626*2362934*677114818445699*1*624892*22792879672*793728131476498189537235765741447**925324*1883662967997814718664975489464**8892674144*918151*168*478758488725*846**817*112*4795*881792289229596242151*9487423156922595*5*262882369675*66*58549177**427*66167514696833*791185*1758*38713414*1866*998454342733**371*3*594822*15*3263*651844*87228142*71478883*1*5541*55***68872678*12493733*482872*37*727978811138179572452*65343367*719*2279*72712156*495*2429767262*43*82416998*227277935911179197826*63794561865267672222*59395**918884*99177*161696865755345543887*511388*879632*37161**271164275176789222*12873329731*62*4243731927527284236786**65*913424499*45491355467*695652459*842748478294781545184186487272189363295351*231186497922324*86867489856262894975488839*53166923943131336971**88*5729534732*8531365462*365844375257716**222713*19*9*75685726311*2*6539*81129588*3711753489882138558*734356168544347853*241*523*9495653628*82454**917831255266871411345656731117*68628755212948333844421376262463267722782764*84621978*71*441155841*95625444115142214*189395118*168*227758612141858*2837643948*577366936379*9*628635764327*445122741856*5665447*389749262561334534552782628696534*443431252*975645219*3923199179119894397*1251*3663885759481562897645718714*5968326446564*64894971555972575*147*88474*63654*593469484284657*199979*5813152871672689136258556*6559*647523*761399352425453*954269*573**76652127483*23192563*639848897897965114739592992171923*97933*997217*59117541*527*275671212561777217379367253512378*5314*57*2*5334748**1851*346994823797541631*9994141171529*7*47173113*51563*937151*42*872546*541452411417*1*1931*9*88382*1423749965917341*43*3649346246487388731114*237569*68*6859**11146258*8*499846733*91965422196*951434966462372738*8168475476333678*12699854*66787646343128334385*8376611825*44422338622*37871683*598932*384*72746512243365695*8379*91*496*23*236*175**779511188964816746867144*6465434*443746***4389287*87391*3*892367358**2*9194962683191*46842482*923438632*29299921535*36974537987*896*28986231752683957149534616896152696279639*14754863*4226*376*878783585531645464*26397*73613769799256166594*9472785662794*24552237458429*168441347749741625377*765367*67648491742264561437418*15243739921899*2854579**3*255994*2*795267195722*8811266279*8888**2621853888149395549964213*534*67279695**38627821958*433851339328844*932*2*137419*674298269298*795655323252564**23943*35947415482*13222352931317479186138112267*846831234*364*175*4773732515332*464368553455191293276*63111489371548633477988*51873226579433768*66844*48889646*4587324*4613469432875466785335*5**6586489736553512399521*2*312981629*3**46*6515644*638556299876813671112*9397626354627937*791158438635147295251969854597*8953**62652249944*232835561172*1863759995564*7*25314917978699*928583688719723347*663889*743145637***8714*297717*438195775818338866797*31*746*312*55*242514214*62*3*2216**86*422733*839148133*95*3*2238851487913574*583325117656*6493289*5462229*8887745331656795147844258*97*19711*5*7*673***25196457**8*2499485*376*8359892265727*73*357834*2692346966*396855*945*245*71*24835555836926571*9161415537114992436528225*957683517523879231*617765611*3682966244792*621*141866476*5985225553248447984**1*247381715165163284918213**2*39628891844847121*4275125*633*46*7*27*5233683375*56248812236**2169*56941475*3*19*9*65*38723**274675*27687135766*367466*26944119953*752*49725174*983643269785*3*9182*9242648239384886733626462692179585779448*4358447323133745417*3783696394*1'], 1),
        (["*********"], 291868912),
        (['**'], 96),
        (['126'], 3),
        (['1261'], 3),
        (['12612'], 3),
        (['***3***1**0****'], 81),
        (['**'], 81),
        (['*'], 9),
        (['1*'], 18),
        ([''.join([random.choice('*') for i in range(10**5)])], 81),
    ]:
        # print case
        res = solution.numDecodings(*case)
        try:
            assert res == ans
        except AssertionError as e:
            status = fail_string(res=res, ans=ans, case=case)
            sys.exit(status)

if __name__ == '__main__':
    test()