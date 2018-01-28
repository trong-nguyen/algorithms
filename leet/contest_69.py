#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

"""



import sys
from utils.templates import fail_string

def merge_count(a, b):
    # if not a and not b:
    #     return 0, []
    # elif not a:
    #     return 0, b
    # elif not b:
    #     return 0, a

    i = 0
    j = 0

    count = 0
    res = []
    m, n = len(a), len(b)
    while i < m and j < n:
        if a[i] < b[j]:
            res.append(a[i])
            i += 1
        else:
            count += m - i
            if m - i > 1:
                return 10000, []
            res.append(b[j])
            j += 1


    if i <= m - 1:
        res += a[i:]
    elif j <= n - 1:
        res += b[j:]

    return count, res

def divide(x):
    if len(x) < 2:
        return 0, x

    count_a, a = divide(x[:len(x)/2])
    count_b, b = divide(x[len(x)/2:])

    # print a, b

    count, c = merge_count(a, b)

    return count + count_a + count_b, c

def local_inverse(x):
    count = 0
    for i in range(1, len(x)):
        if x[i-1] > x[i]:
            count += 1

    return count



class Solution(object):
    def isIdealPermutation(self, A):
        """
        :type A: List[int]
        :rtype: bool
        """
        # g, _ = divide(A)
        # l = local_inverse(A)
        # print g, l
        # return g == l

        if len(A) < 3:
            return True

        if len(A) == 3:
            return A[0] < A[2]

        m = A[0]
        for i in range(2, len(A)):
            if m > A[i]:
                return False

            m = max(m, A[i-1])

        return True



class Solution1(object):
    def numJewelsInStones(self, J, S):
        """
        :type J: str
        :type S: str
        :rtype: int
        """
        if not J:
            return 0

        jewels = set(J)

        js = filter(lambda x: x in jewels, S)

        return len(js)

def test():
    solution = Solution()

    for case, ans in [
        ([[1,0,3,2,4,6,5,8,7,10,9,12,11,14,13,15,16,18,17,19,20,21,23,22,24,25,27,26,28,30,29,32,31,34,33,35,37,36,39,38,40,41,42,44,43,46,45,47,48,50,49,52,51,53,55,54,56,57,59,58,60,62,61,64,63,65,66,68,67,70,69,72,71,74,73,75,76,78,77,80,79,81,83,82,85,84,87,86,89,88,91,90,92,93,95,94,97,96,99,98,101,100,103,102,105,104,106,107,109,108,111,110,112,113,114,116,115,117,118,120,119,122,121,123,125,124,126,127,129,128,131,130,132,134,133,136,135,137,139,138,140,141,142,143,144,146,145,147,148,149,150,152,151,153,154,155,157,156,158,159,160,162,161,164,163,165,166,167,169,168,171,170,173,172,174,176,175,177,178,179,180,181,183,182,184,186,185,188,187,190,189,191,192,193,194,195,196,198,197,200,199,201,202,204,203,206,205,207,208,210,209,212,211,214,213,216,215,218,217,219,221,220,222,224,223,225,227,226,228,229,230,231,233,232,234,235,236,237,239,238,241,240,243,242,244,246,245,248,247,249,250,252,251,254,253,255,257,256,259,258,260,261,263,262,264,266,265,268,267,270,269,271,272,274,273,276,275,278,277,280,279,282,281,283,284,286,285,287,289,288,291,290,292,294,293,296,295,298,297,300,299,302,301,304,303,305,307,306,309,308,310,312,311,314,313,315,317,316,318,319,321,320,323,322,325,324,327,326,329,328,330,332,331,333,334,336,335,337,339,338,341,340,343,342,345,344,347,346,349,348,350,352,351,353,355,354,357,356,358,360,359,362,361,364,363,365,366,367,369,368,370,372,371,373,374,376,375,378,377,380,379,381,382,384,383,385,386,388,387,389,391,390,393,392,394,396,395,398,397,399,401,400,402,403,404,405,406,407,408,409,410,411,413,412,415,414,417,416,419,418,420,422,421,423,425,424,426,428,427,430,429,431,432,434,433,436,435,437,438,439,440,442,441,444,443,445,446,447,449,448,451,450,452,454,453,455,457,456,458,459,460,461,463,462,465,464,466,467,468,469,471,470,472,473,475,474,477,476,479,478,481,480,482,483,484,485,486,487,488,490,489,491,492,493,494,495,497,496,499,498,500,501,503,502,504,506,505,507,508,509,510,512,511,514,513,516,515,518,517,519,521,520,522,524,523,525,527,526,528,530,529,531,532,533,535,534,537,536,538,540,539,542,541,544,543,545,547,546,548,550,549,552,551,553,554,556,555,557,558,559,561,560,563,562,565,564,566,568,567,569,570,572,571,574,573,575,576,577,579,578,581,580,583,582,584,586,585,588,587,589,591,590,592,594,593,595,596,598,597,600,599,601,603,602,605,604,607,606,608,610,609,611,612,613,614,616,615,617,619,618,621,620,622,624,623,625,626,628,627,629,631,630,633,632,635,634,636,638,637,640,639,641,642,643,645,644,647,646,648,650,649,651,652,654,653,655,656,657,658,659,660,661,662,663,664,665,667,666,668,670,669,672,671,673,675,674,676,678,677,679,680,682,681,683,685,684,687,686,689,688,691,690,692,694,693,696,695,697,699,698,700,702,701,704,703,706,705,707,708,709,710,711,713,712,715,714,717,716,719,718,721,720,722,724,723,725,727,726,729,728,730,732,731,734,733,735,736,738,737,739,740,742,741,744,743,746,745,748,747,750,749,752,751,753,754,756,755,757,759,758,761,760,763,762,764,766,765,767,768,769,771,770,773,772,774,775,776,778,777,780,779,782,781,783,784,786,785,788,787,790,789,792,791,794,793,796,795,798,797,800,799,802,801,804,803,805,807,806,809,808,810,811,812,813,814,815,817,816,818,820,819,822,821,824,823,825,827,826,828,829,831,830,832,833,834,835,837,836,838,840,839,841,843,842,844,845,847,846,849,848,850,852,851,853,854,856,855,858,857,860,859,862,861,864,863,865,866,868,867,869,871,870,873,872,874,876,875,877,879,878,881,880,883,882,885,884,887,886,888,889,891,890,892,894,893,895,897,896,899,898,901,900,903,902,905,904,907,906,908,910,909,912,911,913,915,914,916,918,917,920,919,922,921,923,925,924,927,926,929,928,930,932,931,933,934,935,937,936,938,940,939,942,941,943,945,944,947,946,949,948,951,950,952,954,953,955,957,956,958,960,959,961,963,962,965,964,966,967,969,968,970,972,971,974,973,976,975,978,977,980,979,981,983,982,984,986,985,988,987,989,990,992,991,994,993,995,996,998,997,1000,999,1001,1002,1004,1003,1005,1006,1007,1008,1010,1009,1011,1013,1012,1015,1014,1016,1018,1017,1020,1019,1021,1022,1023,1025,1024,1026,1027,1028,1030,1029,1031,1032,1034,1033,1035,1037,1036,1039,1038,1041,1040,1042,1043,1044,1045,1046,1047,1048,1050,1049,1051,1053,1052,1054,1055,1057,1056,1058,1059,1060,1061,1062,1063,1065,1064,1067,1066,1068,1069,1070,1072,1071,1073,1074,1076,1075,1077,1079,1078,1080,1082,1081,1084,1083,1086,1085,1087,1088,1090,1089,1091,1093,1092,1095,1094,1096,1097,1098,1100,1099,1101,1103,1102,1105,1104,1107,1106,1108,1109,1110,1112,1111,1114,1113,1115,1117,1116,1118,1119,1120,1121,1122,1123,1125,1124,1126,1127,1128,1130,1129,1131,1132,1134,1133,1136,1135,1137,1139,1138,1141,1140,1142,1143,1145,1144,1147,1146,1149,1148,1150,1152,1151,1154,1153,1156,1155,1158,1157,1160,1159,1162,1161,1164,1163,1166,1165,1168,1167,1170,1169,1172,1171,1174,1173,1176,1175,1177,1179,1178,1180,1182,1181,1183,1184,1186,1185,1188,1187,1189,1191,1190,1193,1192,1195,1194,1196,1198,1197,1200,1199,1201,1202,1203,1205,1204,1207,1206,1208,1210,1209,1211,1213,1212,1214,1216,1215,1217,1219,1218,1221,1220,1223,1222,1225,1224,1226,1227,1229,1228,1230,1231,1233,1232,1235,1234,1237,1236,1239,1238,1241,1240,1243,1242,1245,1244,1246,1247,1248,1250,1249,1251,1253,1252,1255,1254,1257,1256,1258,1259,1261,1260,1262,1263,1264,1266,1265,1268,1267,1270,1269,1272,1271,1273,1275,1274,1276,1278,1277,1279,1280,1281,1282,1283,1285,1284,1286,1287,1288,1289,1290,1291,1292,1294,1293,1296,1295,1298,1297,1300,1299,1301,1302,1303,1305,1304,1306,1307,1308,1309,1310,1311,1313,1312,1315,1314,1316,1317,1318,1319,1321,1320,1322,1323,1324,1326,1325,1328,1327,1329,1331,1330,1333,1332,1334,1335,1337,1336,1338,1340,1339,1342,1341,1344,1343,1345,1346,1348,1347,1349,1350,1352,1351,1353,1355,1354,1356,1358,1357,1360,1359,1361,1362,1363,1364,1366,1365,1367,1369,1368,1370,1371,1372,1373,1375,1374,1377,1376,1379,1378,1380,1382,1381,1383,1385,1384,1387,1386,1389,1388,1391,1390,1392,1393,1395,1394,1397,1396,1398,1400,1399,1402,1401,1403,1404,1406,1405,1408,1407,1409,1410,1411,1413,1412,1414,1416,1415,1418,1417,1420,1419,1422,1421,1424,1423,1426,1425,1428,1427,1429,1430,1431,1432,1433,1435,1434,1437,1436,1438,1440,1439,1442,1441,1444,1443,1446,1445,1448,1447,1449,1450,1451,1452,1453,1454,1455,1456,1457,1459,1458,1460,1461,1462,1463,1465,1464,1467,1466,1469,1468,1470,1471,1472,1474,1473,1475,1476,1477,1479,1478,1481,1480,1482,1483,1484,1485,1486,1488,1487,1490,1489,1491,1493,1492,1495,1494,1496,1498,1497,1499,1500,1501,1503,1502,1504,1506,1505,1508,1507,1509,1510,1511,1513,1512,1515,1514,1516,1517,1519,1518,1520,1521,1523,1522,1524,1525,1527,1526,1528,1530,1529,1531,1533,1532,1535,1534,1537,1536,1538,1540,1539,1542,1541,1543,1545,1544,1546,1548,1547,1549,1551,1550,1552,1553,1555,1554,1557,1556,1558,1559,1561,1560,1562,1564,1563,1566,1565,1568,1567,1569,1571,1570,1573,1572,1574,1575,1577,1576,1578,1580,1579,1581,1582,1584,1583,1585,1586,1587,1589,1588,1591,1590,1592,1594,1593,1595,1596,1598,1597,1600,1599,1601,1603,1602,1604,1606,1605,1607,1608,1610,1609,1611,1613,1612,1614,1615,1616,1618,1617,1620,1619,1621,1623,1622,1624,1626,1625,1627,1629,1628,1630,1631,1632,1633,1634,1636,1635,1637,1639,1638,1640,1641,1642,1643,1645,1644,1646,1647,1648,1649,1650,1651,1652,1654,1653,1656,1655,1657,1659,1658,1660,1662,1661,1663,1665,1664,1666,1668,1667,1670,1669,1672,1671,1673,1674,1675,1677,1676,1679,1678,1681,1680,1683,1682,1685,1684,1687,1686,1688,1690,1689,1692,1691,1694,1693,1696,1695,1698,1697,1699,1701,1700,1702,1703,1704,1706,1705,1708,1707,1709,1710,1712,1711,1714,1713,1716,1715,1717,1718,1719,1720,1721,1723,1722,1724,1726,1725,1727,1728,1729,1731,1730,1733,1732,1735,1734,1737,1736,1739,1738,1741,1740,1743,1742,1744,1746,1745,1748,1747,1749,1751,1750,1752,1754,1753,1756,1755,1758,1757,1759,1760,1762,1761,1764,1763,1766,1765,1767,1768,1770,1769,1772,1771,1773,1774,1775,1777,1776,1779,1778,1780,1781,1782,1784,1783,1785,1787,1786,1788,1790,1789,1791,1792,1793,1794,1795,1797,1796,1798,1799,1800,1802,1801,1803,1804,1806,1805,1808,1807,1809,1810,1812,1811,1813,1814,1816,1815,1817,1818,1820,1819,1822,1821,1824,1823,1825,1827,1826,1828,1829,1831,1830,1832,1834,1833,1835,1837,1836,1838,1839,1841,1840,1843,1842,1844,1846,1845,1848,1847,1850,1849,1852,1851,1853,1855,1854,1856,1857,1859,1858,1860,1861,1862,1863,1865,1864,1866,1868,1867,1870,1869,1872,1871,1874,1873,1876,1875,1878,1877,1879,1881,1880,1883,1882,1885,1884,1886,1888,1887,1890,1889,1891,1892,1894,1893,1895,1896,1898,1897,1900,1899,1902,1901,1903,1904,1905,1906,1908,1907,1909,1911,1910,1913,1912,1914,1916,1915,1918,1917,1919,1921,1920,1922,1923,1924,1925,1927,1926,1928,1930,1929,1931,1933,1932,1935,1934,1936,1938,1937,1939,1941,1940,1942,1944,1943,1946,1945,1948,1947,1950,1949,1952,1951,1953,1954,1955,1957,1956,1959,1958,1960,1961,1963,1962,1965,1964,1967,1966,1969,1968,1970,1972,1971,1973,1975,1974,1977,1976,1979,1978,1981,1980,1983,1982,1984,1985,1987,1986,1989,1988,1990,1991,1993,1992,1995,1994,1996,1998,1997,1999,2001,2000,2003,2002,2005,2004,2007,2006,2008,2009,2011,2010,2013,2012,2014,2015,2016,2017,2019,2018,2021,2020,2023,2022,2024,2025,2026,2027,2029,2028,2030,2032,2031,2033,2035,2034,2037,2036,2038,2039,2041,2040,2043,2042,2045,2044,2047,2046,2048,2050,2049,2051,2052,2053,2055,2054,2056,2057,2059,2058,2060,2061,2063,2062,2064,2066,2065,2068,2067,2070,2069,2072,2071,2073,2074,2075,2077,2076,2078,2079,2081,2080,2083,2082,2085,2084,2087,2086,2088,2090,2089,2092,2091,2094,2093,2096,2095,2098,2097,2099,2101,2100,2103,2102,2105,2104,2107,2106,2108,2110,2109,2111,2112,2113,2114,2115,2117,2116,2118,2119,2121,2120,2122,2123,2125,2124,2127,2126,2128,2129,2130,2131,2133,2132,2134,2136,2135,2138,2137,2140,2139,2142,2141,2144,2143,2146,2145,2148,2147,2149,2151,2150,2153,2152,2155,2154,2156,2157,2158,2160,2159,2161,2163,2162,2164,2166,2165,2167,2168,2169,2170,2172,2171,2173,2175,2174,2177,2176,2179,2178,2180,2182,2181,2183,2184,2186,2185,2188,2187,2190,2189,2192,2191,2193,2194,2196,2195,2198,2197,2199,2201,2200,2203,2202,2205,2204,2206,2208,2207,2209,2210,2211,2212,2213,2214,2215,2217,2216,2219,2218,2220,2221,2222,2223,2224,2225,2226,2228,2227,2229,2230,2231,2233,2232,2235,2234,2237,2236,2239,2238,2241,2240,2242,2244,2243,2245,2246,2247,2249,2248,2250,2252,2251,2253,2254,2255,2257,2256,2258,2259,2261,2260,2262,2264,2263,2266,2265,2268,2267,2269,2271,2270,2272,2273,2274,2276,2275,2277,2278,2280,2279,2281,2283,2282,2285,2284,2286,2287,2289,2288,2291,2290,2292,2293,2294,2295,2296,2298,2297,2299,2301,2300,2302,2304,2303,2306,2305,2307,2309,2308,2310,2312,2311,2313,2314,2315,2317,2316,2318,2319,2320,2321,2322,2324,2323,2326,2325,2328,2327,2330,2329,2331,2333,2332,2334,2335,2336,2337,2338,2339,2341,2340,2342,2344,2343,2345,2347,2346,2348,2349,2351,2350,2353,2352,2355,2354,2356,2358,2357,2359,2360,2362,2361,2364,2363,2365,2367,2366,2368,2370,2369,2372,2371,2373,2375,2374,2377,2376,2379,2378,2380,2381,2382,2384,2383,2386,2385,2388,2387,2390,2389,2391,2392,2394,2393,2395,2396,2398,2397,2400,2399,2402,2401,2404,2403,2406,2405,2408,2407,2410,2409,2412,2411,2413,2415,2414,2417,2416,2418,2420,2419,2422,2421,2423,2424,2426,2425,2427,2428,2429,2430,2431,2432,2433,2435,2434,2436,2437,2439,2438,2441,2440,2443,2442,2444,2446,2445,2447,2449,2448,2451,2450,2453,2452,2455,2454,2457,2456,2458,2459,2460,2461,2463,2462,2464,2465,2467,2466,2468,2469,2470,2472,2471,2474,2473,2476,2475,2478,2477,2479,2480,2481,2482,2484,2483,2486,2485,2488,2487,2490,2489,2492,2491,2493,2495,2494,2497,2496,2498,2500,2499,2501,2502,2504,2503,2505,2507,2506,2508,2510,2509,2511,2512,2513,2514,2515,2516,2517,2519,2518,2520,2522,2521,2524,2523,2526,2525,2528,2527,2530,2529,2531,2533,2532,2534,2536,2535,2538,2537,2540,2539,2541,2543,2542,2544,2545,2546,2548,2547,2550,2549,2551,2553,2552,2554,2556,2555,2557,2558,2560,2559,2562,2561,2563,2565,2564,2567,2566,2568,2569,2570,2571,2572,2574,2573,2576,2575,2578,2577,2580,2579,2581,2583,2582,2585,2584,2587,2586,2589,2588,2591,2590,2593,2592,2595,2594,2597,2596,2598,2600,2599,2602,2601,2603,2604,2606,2605,2608,2607,2609,2611,2610,2612,2613,2614,2616,2615,2617,2618,2620,2619,2621,2623,2622,2625,2624,2626,2628,2627,2629,2631,2630,2632,2634,2633,2636,2635,2638,2637,2640,2639,2641,2642,2644,2643,2645,2646,2647,2648,2649,2651,2650,2653,2652,2654,2656,2655,2657,2658,2659,2660,2661,2663,2662,2665,2664,2667,2666,2669,2668,2671,2670,2673,2672,2674,2676,2675,2678,2677,2679,2681,2680,2682,2684,2683,2686,2685,2687,2688,2689,2690,2692,2691,2693,2694,2696,2695,2698,2697,2699,2700,2701,2702,2704,2703,2705,2707,2706,2709,2708,2711,2710,2712,2713,2715,2714,2716,2718,2717,2719,2721,2720,2723,2722,2724,2725,2726,2727,2729,2728,2730,2732,2731,2734,2733,2735,2737,2736,2738,2739,2740,2742,2741,2743,2745,2744,2746,2748,2747,2749,2751,2750,2752,2754,2753,2756,2755,2758,2757,2760,2759,2761,2763,2762,2764,2765,2766,2767,2769,2768,2770,2772,2771,2774,2773,2775,2776,2777,2778,2780,2779,2782,2781,2784,2783,2786,2785,2787,2788,2789,2790,2792,2791,2794,2793,2796,2795,2797,2799,2798,2801,2800,2803,2802,2805,2804,2807,2806,2809,2808,2811,2810,2813,2812,2814,2816,2815,2817,2819,2818,2821,2820,2822,2823,2824,2825,2827,2826,2829,2828,2831,2830,2832,2833,2834,2835,2837,2836,2839,2838,2841,2840,2842,2843,2844,2846,2845,2848,2847,2850,2849,2851,2853,2852,2854,2856,2855,2857,2859,2858,2860,2862,2861,2864,2863,2865,2866,2868,2867,2869,2870,2871,2873,2872,2875,2874,2877,2876,2879,2878,2880,2881,2882,2884,2883,2886,2885,2887,2888,2890,2889,2891,2893,2892,2895,2894,2896,2898,2897,2900,2899,2902,2901,2903,2904,2905,2906,2908,2907,2910,2909,2911,2913,2912,2915,2914,2917,2916,2919,2918,2921,2920,2923,2922,2924,2925,2926,2928,2927,2930,2929,2931,2933,2932,2935,2934,2936,2937,2939,2938,2940,2941,2943,2942,2945,2944,2946,2947,2948,2949,2951,2950,2952,2953,2954,2956,2955,2957,2958,2960,2959,2961,2962,2964,2963,2965,2967,2966,2969,2968,2971,2970,2973,2972,2974,2976,2975,2977,2979,2978,2980,2981,2982,2983,2985,2984,2987,2986,2989,2988,2990,2991,2993,2992,2995,2994,2997,2996,2998,2999,3001,3000,3002,3003,3005,3004,3006,3007,3008,3009,3010,3011,3013,3012,3014,3016,3015,3017,3018,3020,3019,3022,3021,3023,3024,3025,3027,3026,3029,3028,3031,3030,3032,3034,3033,3036,3035,3038,3037,3039,3040,3041,3043,3042,3044,3046,3045,3047,3049,3048,3050,3051,3052,3053,3054,3056,3055,3057,3058,3060,3059,3062,3061,3063,3064,3066,3065,3067,3068,3070,3069,3072,3071,3073,3074,3075,3077,3076,3078,3079,3080,3081,3082,3083,3084,3086,3085,3087,3088,3089,3090,3091,3093,3092,3095,3094,3097,3096,3098,3100,3099,3102,3101,3103,3105,3104,3107,3106,3108,3109,3110,3111,3112,3114,3113,3115,3117,3116,3119,3118,3120,3121,3122,3123,3124,3126,3125,3127,3129,3128,3130,3131,3133,3132,3135,3134,3136,3137,3139,3138,3140,3141,3143,3142,3144,3145,3147,3146,3148,3150,3149,3152,3151,3154,3153,3156,3155,3158,3157,3160,3159,3162,3161,3163,3164,3166,3165,3168,3167,3170,3169,3171,3172,3173,3174,3176,3175,3177,3179,3178,3180,3182,3181,3184,3183,3186,3185,3188,3187,3189,3190,3192,3191,3193,3194,3196,3195,3197,3198,3200,3199,3202,3201,3204,3203,3206,3205,3208,3207,3209,3211,3210,3212,3213,3215,3214,3217,3216,3219,3218,3220,3222,3221,3224,3223,3226,3225,3227,3228,3230,3229,3232,3231,3233,3235,3234,3236,3237,3238,3239,3240,3241,3243,3242,3245,3244,3246,3248,3247,3249,3250,3251,3253,3252,3254,3255,3257,3256,3259,3258,3261,3260,3262,3263,3265,3264,3267,3266,3269,3268,3271,3270,3273,3272,3274,3276,3275,3278,3277,3279,3280,3282,3281,3284,3283,3286,3285,3288,3287,3290,3289,3292,3291,3294,3293,3295,3296,3298,3297,3300,3299,3301,3302,3304,3303,3305,3306,3308,3307,3309,3310,3312,3311,3313,3315,3314,3316,3318,3317,3319,3321,3320,3322,3324,3323,3325,3326,3327,3328,3329,3331,3330,3333,3332,3335,3334,3336,3337,3338,3340,3339,3342,3341,3344,3343,3345,3346,3347,3349,3348,3350,3352,3351,3353,3355,3354,3356,3357,3359,3358,3361,3360,3362,3363,3365,3364,3367,3366,3369,3368,3371,3370,3372,3374,3373,3375,3377,3376,3378,3379,3380,3381,3382,3383,3385,3384,3386,3388,3387,3390,3389,3391,3392,3394,3393,3395,3397,3396,3398,3399,3400,3402,3401,3404,3403,3406,3405,3407,3409,3408,3410,3411,3412,3414,3413,3415,3416,3417,3418,3420,3419,3421,3423,3422,3425,3424,3427,3426,3429,3428,3430,3431,3433,3432,3434,3435,3436,3438,3437,3440,3439,3442,3441,3443,3445,3444,3446,3448,3447,3449,3450,3451,3452,3453,3455,3454,3457,3456,3458,3459,3460,3462,3461,3464,3463,3466,3465,3468,3467,3470,3469,3471,3472,3474,3473,3476,3475,3478,3477,3480,3479,3482,3481,3484,3483,3485,3487,3486,3488,3489,3491,3490,3492,3494,3493,3495,3496,3498,3497,3500,3499,3502,3501,3503,3505,3504,3506,3507,3508,3509,3511,3510,3513,3512,3515,3514,3516,3517,3519,3518,3520,3522,3521,3524,3523,3525,3527,3526,3529,3528,3531,3530,3533,3532,3534,3536,3535,3537,3539,3538,3541,3540,3542,3543,3544,3545,3547,3546,3549,3548,3551,3550,3553,3552,3555,3554,3557,3556,3559,3558,3561,3560,3562,3563,3564,3565,3567,3566,3569,3568,3571,3570,3573,3572,3575,3574,3576,3578,3577,3580,3579,3582,3581,3584,3583,3585,3587,3586,3588,3589,3591,3590,3593,3592,3595,3594,3597,3596,3598,3600,3599,3602,3601,3603,3604,3606,3605,3607,3608,3610,3609,3612,3611,3614,3613,3615,3616,3618,3617,3620,3619,3622,3621,3624,3623,3625,3626,3628,3627,3630,3629,3632,3631,3633,3634,3636,3635,3637,3638,3639,3641,3640,3642,3644,3643,3645,3647,3646,3648,3649,3650,3651,3653,3652,3654,3655,3657,3656,3659,3658,3660,3662,3661,3663,3664,3665,3667,3666,3668,3670,3669,3672,3671,3673,3674,3676,3675,3678,3677,3679,3681,3680,3682,3684,3683,3685,3687,3686,3689,3688,3691,3690,3693,3692,3694,3695,3697,3696,3698,3699,3701,3700,3703,3702,3704,3705,3706,3707,3708,3709,3710,3711,3712,3714,3713,3715,3716,3718,3717,3720,3719,3721,3722,3724,3723,3725,3726,3728,3727,3729,3731,3730,3733,3732,3735,3734,3737,3736,3738,3740,3739,3742,3741,3743,3745,3744,3746,3747,3749,3748,3750,3752,3751,3754,3753,3755,3756,3757,3758,3759,3761,3760,3763,3762,3765,3764,3766,3767,3768,3769,3771,3770,3772,3773,3774,3776,3775,3778,3777,3780,3779,3782,3781,3784,3783,3785,3787,3786,3789,3788,3791,3790,3792,3793,3794,3796,3795,3797,3799,3798,3801,3800,3802,3803,3804,3806,3805,3807,3808,3810,3809,3812,3811,3814,3813,3816,3815,3817,3819,3818,3821,3820,3822,3824,3823,3825,3827,3826,3829,3828,3831,3830,3833,3832,3835,3834,3836,3837,3839,3838,3840,3841,3843,3842,3845,3844,3846,3847,3849,3848,3850,3852,3851,3854,3853,3855,3857,3856,3858,3859,3860,3862,3861,3864,3863,3866,3865,3868,3867,3870,3869,3872,3871,3873,3874,3875,3877,3876,3879,3878,3881,3880,3882,3883,3885,3884,3887,3886,3889,3888,3891,3890,3892,3894,3893,3895,3897,3896,3899,3898,3901,3900,3902,3903,3904,3906,3905,3908,3907,3910,3909,3911,3912,3914,3913,3916,3915,3918,3917,3920,3919,3921,3922,3924,3923,3925,3927,3926,3928,3929,3931,3930,3933,3932,3935,3934,3936,3938,3937,3939,3941,3940,3942,3943,3945,3944,3947,3946,3949,3948,3950,3951,3953,3952,3955,3954,3957,3956,3958,3959,3961,3960,3962,3964,3963,3965,3966,3967,3968,3969,3971,3970,3972,3973,3974,3975,3976,3978,3977,3979,3981,3980,3983,3982,3984,3985,3986,3988,3987,3990,3989,3991,3993,3992,3994,3996,3995,3998,3997,4000,3999,4001,4003,4002,4004,4006,4005,4007,4008,4009,4011,4010,4013,4012,4015,4014,4017,4016,4018,4020,4019,4021,4023,4022,4024,4026,4025,4028,4027,4030,4029,4031,4032,4034,4033,4035,4037,4036,4038,4040,4039,4042,4041,4043,4044,4046,4045,4047,4048,4050,4049,4052,4051,4054,4053,4056,4055,4058,4057,4060,4059,4061,4062,4064,4063,4065,4066,4068,4067,4069,4071,4070,4073,4072,4075,4074,4077,4076,4079,4078,4081,4080,4083,4082,4085,4084,4087,4086,4088,4090,4089,4091,4092,4094,4093,4096,4095,4097,4099,4098,4101,4100,4102,4104,4103,4105,4107,4106,4108,4109,4111,4110,4112,4113,4115,4114,4117,4116,4119,4118,4120,4122,4121,4124,4123,4126,4125,4127,4128,4130,4129,4132,4131,4133,4134,4136,4135,4137,4138,4139,4140,4141,4143,4142,4144,4145,4147,4146,4148,4150,4149,4151,4152,4154,4153,4156,4155,4157,4158,4160,4159,4161,4163,4162,4164,4165,4166,4168,4167,4169,4171,4170,4172,4173,4174,4175,4176,4178,4177,4179,4181,4180,4182,4183,4185,4184,4187,4186,4188,4189,4190,4191,4193,4192,4195,4194,4196,4198,4197,4199,4200,4201,4203,4202,4205,4204,4207,4206,4208,4209,4211,4210,4212,4214,4213,4215,4217,4216,4219,4218,4221,4220,4222,4224,4223,4225,4227,4226,4228,4229,4230,4231,4233,4232,4235,4234,4237,4236,4239,4238,4241,4240,4242,4243,4245,4244,4247,4246,4248,4249,4250,4252,4251,4254,4253,4255,4256,4258,4257,4259,4261,4260,4262,4264,4263,4265,4266,4267,4269,4268,4270,4271,4272,4274,4273,4275,4277,4276,4278,4280,4279,4281,4283,4282,4285,4284,4286,4288,4287,4289,4291,4290,4293,4292,4294,4295,4297,4296,4299,4298,4300,4301,4303,4302,4304,4305,4307,4306,4309,4308,4311,4310,4313,4312,4314,4316,4315,4318,4317,4319,4321,4320,4322,4324,4323,4326,4325,4327,4329,4328,4331,4330,4332,4334,4333,4336,4335,4337,4338,4339,4340,4341,4342,4344,4343,4346,4345,4348,4347,4349,4351,4350,4352,4354,4353,4356,4355,4358,4357,4360,4359,4362,4361,4364,4363,4366,4365,4368,4367,4370,4369,4371,4372,4374,4373,4375,4376,4378,4377,4380,4379,4381,4383,4382,4384,4385,4386,4388,4387,4389,4390,4392,4391,4394,4393,4396,4395,4398,4397,4400,4399,4401,4402,4404,4403,4405,4406,4408,4407,4410,4409,4412,4411,4414,4413,4416,4415,4418,4417,4420,4419,4422,4421,4423,4424,4426,4425,4427,4429,4428,4431,4430,4433,4432,4435,4434,4437,4436,4439,4438,4441,4440,4443,4442,4444,4445,4447,4446,4448,4450,4449,4451,4452,4453,4454,4456,4455,4457,4459,4458,4460,4462,4461,4463,4465,4464,4467,4466,4468,4470,4469,4471,4472,4474,4473,4476,4475,4478,4477,4479,4480,4482,4481,4483,4485,4484,4486,4488,4487,4489,4491,4490,4493,4492,4495,4494,4497,4496,4498,4500,4499,4502,4501,4504,4503,4505,4506,4508,4507,4510,4509,4511,4512,4514,4513,4515,4517,4516,4518,4520,4519,4521,4522,4523,4524,4526,4525,4527,4528,4530,4529,4531,4533,4532,4534,4535,4537,4536,4538,4539,4540,4542,4541,4543,4545,4544,4546,4547,4549,4548,4550,4551,4552,4554,4553,4556,4555,4557,4559,4558,4560,4561,4563,4562,4565,4564,4566,4567,4569,4568,4571,4570,4573,4572,4575,4574,4576,4577,4579,4578,4581,4580,4583,4582,4585,4584,4587,4586,4589,4588,4590,4591,4593,4592,4595,4594,4596,4597,4599,4598,4600,4602,4601,4603,4605,4604,4606,4607,4609,4608,4611,4610,4613,4612,4615,4614,4616,4617,4619,4618,4620,4621,4622,4624,4623,4626,4625,4627,4628,4629,4630,4631,4633,4632,4634,4635,4637,4636,4639,4638,4640,4642,4641,4643,4644,4646,4645,4647,4649,4648,4651,4650,4652,4653,4654,4656,4655,4658,4657,4659,4661,4660,4662,4663,4665,4664,4666,4667,4668,4669,4670,4671,4672,4673,4674,4676,4675,4678,4677,4679,4681,4680,4682,4684,4683,4685,4687,4686,4689,4688,4691,4690,4692,4694,4693,4695,4696,4697,4698,4700,4699,4702,4701,4704,4703,4705,4707,4706,4709,4708,4711,4710,4713,4712,4714,4715,4717,4716,4718,4719,4721,4720,4722,4723,4724,4725,4727,4726,4728,4730,4729,4731,4733,4732,4734,4736,4735,4737,4739,4738,4740,4741,4743,4742,4744,4746,4745,4748,4747,4750,4749,4751,4753,4752,4755,4754,4756,4757,4759,4758,4760,4761,4762,4763,4765,4764,4767,4766,4768,4770,4769,4771,4772,4773,4774,4775,4776,4777,4779,4778,4780,4781,4783,4782,4785,4784,4787,4786,4789,4788,4790,4792,4791,4794,4793,4795,4796,4797,4799,4798,4801,4800,4803,4802,4805,4804,4806,4807,4809,4808,4810,4812,4811,4813,4814,4815,4816,4817,4819,4818,4820,4822,4821,4823,4824,4826,4825,4827,4828,4830,4829,4831,4832,4833,4834,4835,4837,4836,4839,4838,4841,4840,4842,4843,4845,4844,4846,4847,4848,4849,4851,4850,4853,4852,4854,4856,4855,4857,4859,4858,4860,4862,4861,4863,4864,4866,4865,4867,4868,4870,4869,4871,4873,4872,4875,4874,4877,4876,4878,4879,4881,4880,4883,4882,4884,4886,4885,4887,4888,4889,4891,4890,4892,4893,4895,4894,4897,4896,4899,4898,4900,4901,4903,4902,4904,4905,4906,4908,4907,4910,4909,4912,4911,4914,4913,4916,4915,4917,4919,4918,4921,4920,4923,4922,4925,4924,4926,4928,4927,4930,4929,4931,4932,4934,4933,4935,4937,4936,4938,4940,4939,4941,4942,4943,4945,4944,4946,4947,4949,4948,4950,4952,4951,4954,4953,4955,4957,4956,4958,4959,4960,4961,4963,4962,4965,4964,4966,4967,4969,4968,4970,4972,4971,4974,4973,4976,4975,4977,4978,4979,4980,4982,4981,4984,4983,4985,4987,4986,4989,4988,4990,4992,4991,4993,4994,4995,4997,4996,4998,4999]], True),
        ([[1]], True),
        ([[1, 0, 2]], True),
        ([[1, 2, 0]], False),
    ]:
        res = solution.isIdealPermutation(*case)
        try:
            assert res == ans
        except AssertionError as e:
            status = fail_string(res=res, ans=ans, case=case)
            sys.exit(status)

def test1():
    solution = Solution()
    for case, ans in [
        (['', ''], 0),
        (['a', 'aaa'], 3),
        (['aA', 'aAAbbbb'], 3),
        (['z', 'ZZ'], 0),
    ]:
        res = solution.numJewelsInStones(*case)
        try:
            assert res == ans
        except AssertionError as e:
            status = fail_string(res=res, ans=ans, case=case)
            sys.exit(status)

if __name__ == '__main__':
    test()