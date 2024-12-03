[![Documentation Status](https://readthedocs.org/projects/queryhyperleda/badge/?version=latest)](https://queryhyperleda.readthedocs.io/en/latest/?badge=latest)

# Query HyperLEDA (query.hyperleda)

Query from the HyperLEDA web data access service

---------
(NB: I'm making this module available for an early use, while waiting for PR review <a href="https://github.com/astropy/astroquery/pull/2023">2023</a> to <a href="https://github.com/astropy/astroquery">astroquery</a>).

---------
## Brief description

This module can be used to query from the <a href="http://leda.univ-lyon1.fr/">HyperLEDA</a> web service. 
The queries will return the results<br>in an astropy <a href="https://docs.astropy.org/en/stable/api/astropy.table.Table.html#astropy.table.Table">Table</a>. Below are two working examples illustrating how to retrieve data for a single object,<br>or using an SQL query request to the <a href="http://leda.univ-lyon1.fr/fullsql.html">HyperLEDA SQL data access service</a>.

# Examples
-------

## Query an object

Query the object by name. For instance if you want to query UGC 1259



```python

>>> from query import hyperleda

>>> result_table = hyperleda.query_object('UGC12591' , properties='all')
>>> print(result_table) # an astropy.table.Table

```

     pgc  objname  objtype ...   celposB(pgc)     celposJ(pgc)  
    ----- -------- ------- ... ---------------- ----------------
    71392 UGC12591       G ... B232253.7+281313 J232521.9+282943


-----------
To see all available <code>properties</code> that HyperLEDA returns:


```python
>>> properties_tbl = hyperleda.get_properties()
>>> properties_tbl.pprint_all()
```

        field      type       units                                         description                                   
    ------------- ------ --------------- ---------------------------------------------------------------------------------
              pgc    int              --                                                                        PGC number
          objname   char              --                                                                    Principal name
          objtype   char              --                                             Type of object (G=galaxy; S=Star ...)
           al1950 double            hour                                                     RA 1950 (hours decimal value)
           de1950 double             deg                                                  DEC 1950 (degrees decimal value)
           al2000 double            hour                                                     RA 2000 (hours decimal value)
           de2000 double             deg                                                  DEC 2000 (degrees decimal value)
               l2 double             deg                                                                Galactic longitude
               b2 double             deg                                                                 Galactic latitude
              sgl double             deg                                                           Supergalactic longitude
              sgb double             deg                                                            Supergalactic latitude
             type   char              --                                                                Morphological type
              bar   char              --                                                                 Barred galaxy (B)
             ring   char              --                                                              Galaxy with ring (R)
         multiple   char              --                                                               Multiple galaxy (M)
      compactness   char              --                                                        Compact (C) or diffuse (D)
                t  float              --                                                           Morphological type code
              e_t  float              --                                       Actual error on t (Morphological type code)
           logd25  float log(0.1 arcmin)                                      log of apparent diameter (d25 in 0.1 arcmin)
         e_logd25  float log(0.1 arcmin)                   Actual error on logd25 (log of apparent diameter in 0.1 arcmin)
           logr25  float             log                                         log of axis ratio (major axis/minor axis)
         e_logr25  float             log                 Actual error on logr25 (log of axis ratio: major axis/minor axis)
               pa  float             deg                                       Major axis position angle (North Eastwards)
            brief  float     mag/arcsec2                                                 Mean effective surface brightness
          e_brief  float     mag/arcsec2                         Actual error on brief (Mean effective surface brightness)
               bt  float             mag                                                                 Total B-magnitude
             e_bt  float             mag                                            Actual error on bt (Total B-magnitude)
               it  float             mag                                                                 Total I-magnitude
             e_it  float             mag                                            Actual error on it (Total I-magnitude)
               ut  float             mag                                                                 Total U-magnitude
               vt  float             mag                                                                 Total V-magnitude
              ube  float             mag                                                               Effective U-B color
              bve  float             mag                                                               Effective B-V color
            vmaxg  float            km/s                                         Apparent maximum rotation velocity of gas
          e_vmaxg  float            km/s                 Actual error on vmaxg (Apparent maximum rotation velocity of gas)
            vmaxs  float            km/s                                       Apparent maximum rotation velocity of stars
          e_vmaxs  float            km/s               Actual error on vmaxs (Apparent maximum rotation velocity of stars)
             vdis  float            km/s                                                       Central velocity dispersion
           e_vdis  float            km/s                                Actual error on vdis (Central velocity dispersion)
              m21  float             mag                                                      21-cm line flux in magnitude
            e_m21  float             mag                                Actual error on m21 (21-cm line flux in magnitude)
             mfir  float             mag                                                            Far infrared magnitude
             vrad  float            km/s                          Heliocentric radial velocity (cz) from radio measurement
           e_vrad  float            km/s   Actual error on vrad (Heliocentric radial velocity (cz) from radio measurement)
             vopt  float            km/s                        Heliocentric radial velocity (cz) from optical measurement
           e_vopt  float            km/s Actual error on vopt (Heliocentric radial velocity (cz) from optical measurement)
                v  float            km/s                                            Mean Heliocentric radial velocity (cz)
              e_v  float            km/s                             Actual error on v (Mean Heliocentric radial velocity)
               ag  float             mag                                                     Galactic extinction in B-band
               ai  float             mag                                  Internal extinction due to inclination in B-band
             incl  float             deg                      Inclination between line of sight and polar axis of a galaxy
              a21  float             mag                                                             21-cm self absorption
            logdc  float log(0.1 arcmin)                             log of apparent corrected diameter (dc in 0.1 arcmin)
              btc  float             mag                                              Total apparent corrected B-magnitude
              itc  float             mag                                              Total apparent corrected I-magnitude
             ubtc  float             mag                                                Total apparent corrected U-B color
             bvtc  float             mag                                                Total apparent corrected B-V color
            bri25  float     mag/arcsec2                                        Mean surface brightness within isophote 25
             vrot  float            km/s                               Maximum rotation velocity corrected for inclination
           e_vrot  float            km/s        Actual error on vrot (Maximum rotation velocity corrected for inclination)
              mg2  float             mag                                                            Central Lick Mg2 index
            e_mg2  float             mag                                     Actual error on mg2( Central Lick Mg2 index )
          logavmm  float              --                                                                                --
        e_logavmm  float              --                                                                                --
             m21c  float             mag                                            Corrected 21-cm line flux in magnitude
              hic  float             mag                                                 21-cm index btc-m21c in magnitude
              vlg  float            km/s                              Radial velocity (cz) with respect to the Local Group
             vgsr  float            km/s                                      Radial velocity (cz) with respect to the GSR
             vvir  float            km/s                           Radial velocity (cz) corrected for LG infall onto Virgo
              v3k  float            km/s                            Radial velocity (cz) with respect to the CMB radiation
             modz  float             mag                               Cosmological distance modulus (from vvir with ΛCDM)
             mod0  float             mag                                       Distance modulus from distance measurements
             mabs  float             mag                                                         Absolute B-band magnitude
          numtype   char              --                                                                                --
             hptr   char              --                                                                                --
         agnclass   char              --                                                             Activity class of AGN
         f_astrom   char              --                                                      Precision flag on astrometry
           e_mod0  float             mag                Actual error on mod0 (Distance modulus from distance measurements)
           e_modz  float             mag          Actual error on modz (Cosmological distance modulus from vvir with ΛCDM)
           e_mabs  float              --                                                                                --
          modbest  float             mag                                    Best distance modulus, combining mod0 and modz
        e_modbest  float             mag          Actual error on modbest (Best distance modulus, combining mod0 and modz)
               kt  float             mag                                                                 Total K-magnitude
             e_kt  float             mag                                            Actual error on kt (Total K-magnitude)
             e_ut  float             mag                                            Actual error on ut (Total U-magnitude)
             e_vt  float             mag                                            Actual error on vt (Total V-magnitude)
    hl_names(pgc) string              --                 Comma separated list of all the designations for the object "pgc"
     celposB(pgc) string              --         Return the B1950 celestial position of object "pgc" in sexagesimal format
     celposJ(pgc) string              --         Return the J2000 celestial position of object "pgc" in sexagesimal format


_________


Retrieve only a subset from the available <code>properties</code>:



```python

>>> result_table = hyperleda.query_object('UGC12591' , properties='objname, type,\
                                      logr25, btc, v, modbest, al2000, de2000,\
                                      celposJ(pgc)')
>>> result_table.pprint_all()
```

    objname  type logr25  btc     v    modbest   al2000     de2000     celposJ(pgc)  
    -------- ---- ------ ------ ------ ------- ---------- ---------- ----------------
    UGC12591 S0-a  0.354 13.174 6939.5  35.067 23.4227381 28.4951858 J232521.9+282943


----------
## Query using SQL syntax

An example for querying using SQL WHERE clause syntax as in <a href="http://leda.univ-lyon1.fr/fullsql.html">HyperLEDA (http://leda.univ-lyon1.fr/fullsql.html)</a>.<br>


```python
# The SQL sample_query is the WHERE clause is to filter by properties
>>> sample_query = "(modbest<=30 and t>=-3 and t<=0 and type='S0') \
or (modbest<=30 and t>=-3 and t<=0 and type='S0-a')"

# Select some properties to retrieve
>>> sample_properties= 'objname, al2000, de2000, type, logr25, btc, e_bt, v, modbest'

# Run the query
>>> result_table = hyperleda.query_sql(sample_query, properties=sample_properties)
```


```python
>>> result_table.pprint(max_lines=5, max_width=-1)
```

     objname     al2000     de2000   type logr25  btc    e_bt   v   modbest
    ---------- ---------- ---------- ---- ------ ------ ----- ----- -------
       NGC4488 12.5142721  8.3600991 S0-a  0.562  12.65 0.103 980.1  29.775
       NGC4659    12.7415 13.4985547 S0-a   0.15 12.787 0.035 464.1   29.81
           ...        ...        ...  ...    ...    ...   ...   ...     ...
    PGC1420152 11.3733367 12.9795655   S0  0.048 16.654   0.5 564.1  29.942
       NGC5455 14.0503204 54.2414569   S0   0.11 15.175   0.5 259.9   29.67
    Length = 19 rows

