"""
Generate PublicHealthDashboard.twb — Final corrected version.
Workbook element content model:
  (preferences?, datasources?, actions?, worksheets?, dashboards?, windows, ...)
"""
import os, html

BASE        = "/Users/manjotkaur/Downloads/project dv"
COUNTY_CSV  = os.path.join(BASE, "data/cleaned/cdc_places_county_clean.csv")
HEATMAP_CSV = os.path.join(BASE, "data/cleaned/heatmap_state_conditions.csv")
OUT         = os.path.join(BASE, "tableau/PublicHealthDashboard.twb")

DS_C   = "federated.county001"
DS_H   = "federated.heat001"
NC_C   = "textscan.county001"
NC_H   = "textscan.heat001"

CALC     = "[Calculation_SelectedMeasure]"
CALC_USR = "[usr:Calculation_SelectedMeasure:qk]"
PARAM    = "[Parameter 1]"

FX = html.escape(
    'IF [Parameters].[Parameter 1] = "Diabetes" THEN [Diabetes_AdjPrev]\n'
    'ELSEIF [Parameters].[Parameter 1] = "Obesity" THEN [Obesity_AdjPrev]\n'
    'ELSEIF [Parameters].[Parameter 1] = "High Blood Pressure" THEN [BPHIGH_AdjPrev]\n'
    'ELSEIF [Parameters].[Parameter 1] = "Mental Health (Poor Days)" THEN [MHLTH_AdjPrev]\n'
    'ELSEIF [Parameters].[Parameter 1] = "Sleep Less Than 7h" THEN [SLEEP_AdjPrev]\n'
    'END'
)

def meta(name, rtype, ordinal, agg, parent):
    is_str = (rtype == 129)
    extra = (
        f"<local-type>string</local-type><aggregation>{agg}</aggregation>"
        "<scale>1</scale><width>1073741823</width><contains-null>true</contains-null>"
    ) if is_str else (
        f"<local-type>real</local-type><aggregation>{agg}</aggregation>"
        "<contains-null>true</contains-null>"
    )
    return f"""          <metadata-record class='column'>
            <remote-name>{name}</remote-name><remote-type>{rtype}</remote-type>
            <local-name>[{name}]</local-name><parent-name>[{parent}]</parent-name>
            <remote-alias>{name}</remote-alias><ordinal>{ordinal}</ordinal>
            {extra}
          </metadata-record>"""

PARAMS = """<members>
            <member alias='Diabetes'                  value='Diabetes' />
            <member alias='Obesity'                   value='Obesity' />
            <member alias='High Blood Pressure'       value='High Blood Pressure' />
            <member alias='Mental Health (Poor Days)' value='Mental Health (Poor Days)' />
            <member alias='Sleep Less Than 7h'        value='Sleep Less Than 7h' />
          </members>"""

def param_dep(indent="          "):
    return f"""{indent}<datasource-dependencies datasource='Parameters'>
{indent}  <column caption='Select Health Measure' datatype='string' name='{PARAM}'
{indent}          param-domain-type='list' role='measure' type='nominal' value='Diabetes'>
{indent}    {PARAMS}
{indent}  </column>
{indent}</datasource-dependencies>"""

def calc_col(indent="            "):
    return f"""{indent}<column caption='Selected Measure Value' datatype='real'
{indent}        name='{CALC}' role='measure' type='quantitative'>
{indent}  <calculation class='tableau' formula='{FX}' />
{indent}</column>"""

twb = f"""<?xml version='1.0' encoding='utf-8' ?>
<workbook locale='en_US' source-build='2026.1.0' source-platform='mac' version='18.1'
          xmlns:user='http://www.tableausoftware.com/xml/user'>
  <preferences>
    <preference name='ui.encoding.shelf.height' value='24' />
    <preference name='ui.shelf.height' value='26' />
  </preferences>

  <!-- ════════════════════════════════════════════════════════════ -->
  <!-- DATA SOURCES (before actions, before worksheets)             -->
  <!-- ════════════════════════════════════════════════════════════ -->
  <datasources>
    <datasource name='Parameters'>
      <column caption='Select Health Measure' datatype='string' name='{PARAM}'
              param-domain-type='list' role='measure' type='nominal' value='Diabetes'>
        {PARAMS}
      </column>
    </datasource>
    <datasource caption='CDC Places County' inline='true' name='{DS_C}' version='18.1'>
      <connection class='federated'>
        <named-connections>
          <named-connection caption='cdc_places_county_clean' name='{NC_C}'>
            <connection auto-extract='yes' character-set='UTF-8' class='textscan'
                        filename='{COUNTY_CSV}' force-character-set='no'
                        force-header='no' force-separator='no' header='yes'
                        separator=',' text-qualifier='&quot;' />
          </named-connection>
        </named-connections>
        <relation connection='{NC_C}' name='cdc_places_county_clean#csv'
                  table='[cdc_places_county_clean#csv]' type='table'>
          <columns character-set='UTF-8' header='yes' locale='en_US'
                   separator=',' text-qualifier='&quot;'>
            <column datatype='string' name='CountyFIPS'       ordinal='0' />
            <column datatype='string' name='StateAbbr'        ordinal='1' />
            <column datatype='string' name='StateDesc'        ordinal='2' />
            <column datatype='string' name='LocationName'     ordinal='3' />
            <column datatype='real'   name='BPHIGH_AdjPrev'   ordinal='4' />
            <column datatype='real'   name='Diabetes_AdjPrev' ordinal='5' />
            <column datatype='real'   name='MHLTH_AdjPrev'    ordinal='6' />
            <column datatype='real'   name='Obesity_AdjPrev'  ordinal='7' />
            <column datatype='real'   name='SLEEP_AdjPrev'    ordinal='8' />
          </columns>
        </relation>
        <refresh increment-key='' incremental-updates='false' />
        <metadata-records>
{meta("CountyFIPS",       129, 0, "Count", "cdc_places_county_clean#csv")}
{meta("StateAbbr",        129, 1, "Count", "cdc_places_county_clean#csv")}
{meta("StateDesc",        129, 2, "Count", "cdc_places_county_clean#csv")}
{meta("LocationName",     129, 3, "Count", "cdc_places_county_clean#csv")}
{meta("BPHIGH_AdjPrev",   5,   4, "Sum",   "cdc_places_county_clean#csv")}
{meta("Diabetes_AdjPrev", 5,   5, "Sum",   "cdc_places_county_clean#csv")}
{meta("MHLTH_AdjPrev",    5,   6, "Sum",   "cdc_places_county_clean#csv")}
{meta("Obesity_AdjPrev",  5,   7, "Sum",   "cdc_places_county_clean#csv")}
{meta("SLEEP_AdjPrev",    5,   8, "Sum",   "cdc_places_county_clean#csv")}
        </metadata-records>
      </connection>
      <aliases enabled='yes' />
      <column datatype='string' name='[CountyFIPS]'   role='dimension'
              semantic-role='[County].[FIPS]'   type='ordinal' />
      <column datatype='string' name='[StateAbbr]'    role='dimension' type='nominal' />
      <column datatype='string' name='[StateDesc]'    role='dimension'
              semantic-role='[State].[Name]'    type='nominal' />
      <column datatype='string' name='[LocationName]' role='dimension' type='nominal' />
      <column datatype='real' name='[BPHIGH_AdjPrev]'   role='measure' type='quantitative' />
      <column datatype='real' name='[Diabetes_AdjPrev]' role='measure' type='quantitative' />
      <column datatype='real' name='[MHLTH_AdjPrev]'    role='measure' type='quantitative' />
      <column datatype='real' name='[Obesity_AdjPrev]'  role='measure' type='quantitative' />
      <column datatype='real' name='[SLEEP_AdjPrev]'    role='measure' type='quantitative' />
      <column caption='Selected Measure Value' datatype='real'
              name='{CALC}' role='measure' type='quantitative'>
        <calculation class='tableau' formula='{FX}' />
      </column>
    </datasource>
    <datasource caption='Heatmap State Conditions' inline='true' name='{DS_H}' version='18.1'>
      <connection class='federated'>
        <named-connections>
          <named-connection caption='heatmap_state_conditions' name='{NC_H}'>
            <connection auto-extract='yes' character-set='UTF-8' class='textscan'
                        filename='{HEATMAP_CSV}' force-character-set='no'
                        force-header='no' force-separator='no' header='yes'
                        separator=',' text-qualifier='&quot;' />
          </named-connection>
        </named-connections>
        <relation connection='{NC_H}' name='heatmap_state_conditions#csv'
                  table='[heatmap_state_conditions#csv]' type='table'>
          <columns character-set='UTF-8' header='yes' locale='en_US'
                   separator=',' text-qualifier='&quot;'>
            <column datatype='string' name='StateDesc' ordinal='0' />
            <column datatype='string' name='StateAbbr' ordinal='1' />
            <column datatype='real'   name='Value'     ordinal='2' />
            <column datatype='string' name='Condition' ordinal='3' />
          </columns>
        </relation>
        <refresh increment-key='' incremental-updates='false' />
        <metadata-records>
{meta("StateDesc", 129, 0, "Count", "heatmap_state_conditions#csv")}
{meta("StateAbbr", 129, 1, "Count", "heatmap_state_conditions#csv")}
{meta("Value",     5,   2, "Sum",   "heatmap_state_conditions#csv")}
{meta("Condition", 129, 3, "Count", "heatmap_state_conditions#csv")}
        </metadata-records>
      </connection>
      <aliases enabled='yes' />
      <column datatype='string' name='[StateDesc]' role='dimension'
              semantic-role='[State].[Name]' type='nominal' />
      <column datatype='string' name='[StateAbbr]' role='dimension' type='nominal' />
      <column datatype='real'   name='[Value]'     role='measure'   type='quantitative' />
      <column datatype='string' name='[Condition]' role='dimension' type='nominal' />
    </datasource>
  </datasources>

  <!-- ════════════════════════════════════════════════════════════ -->
  <!-- ACTIONS                                                      -->
  <!-- ════════════════════════════════════════════════════════════ -->
  <actions>
    <action caption='Map to Bar Chart' name='[Action1]'>
      <activation auto-clear='true' type='on-select' />
      <source dashboard='Public Health Dashboard' type='sheet' worksheet='County Map' />
      <command command='tsc:tsl-filter'>
        <param name='special-fields' value='all' />
        <param name='target' value='Public Health Dashboard' />
      </command>
    </action>
    <action caption='State Highlight' name='[Action2]'>
      <activation auto-clear='true' type='on-select' />
      <source dashboard='Public Health Dashboard' type='sheet' />
      <command command='tsc:brush'>
        <param name='field-captions' value='State' />
        <param name='target' value='Public Health Dashboard' />
      </command>
    </action>
  </actions>

  <!-- ════════════════════════════════════════════════════════════ -->
  <!-- WORKSHEETS                                                   -->
  <!-- ════════════════════════════════════════════════════════════ -->
  <worksheets>
    <worksheet name='County Map'>
      <layout-options>
        <title><formatted-text><run fontname='Tableau Semibold'>County Map</run></formatted-text></title>
      </layout-options>
      <table>
        <view>
          <datasources>
            <datasource caption='CDC Places County' name='{DS_C}' />
            <datasource name='Parameters' />
          </datasources>
{param_dep()}
          <datasource-dependencies datasource='{DS_C}'>
            <column datatype='string' name='[CountyFIPS]' role='dimension'
                    semantic-role='[County].[FIPS]' type='ordinal' />
            <column datatype='string' name='[LocationName]' role='dimension' type='nominal' />
            <column datatype='string' name='[StateDesc]' role='dimension'
                    semantic-role='[State].[Name]' type='nominal' />
{calc_col()}
            <column-instance column='[CountyFIPS]' derivation='None'
                             name='[none:CountyFIPS:nk]' pivot='key' type='nominal' />
            <column-instance column='{CALC}' derivation='User'
                             name='{CALC_USR}' pivot='key' type='quantitative' />
          </datasource-dependencies>
          <aggregation value='true' />
        </view>
        <style />
        <panes>
          <pane>
            <view><breakdown value='auto' /></view>
            <mark class='Multipolygon' />
            <mark-sizing mark-sizing-setting='marks-scaling-off' />
            <encodings>
              <color column='[{DS_C}].{CALC_USR}' />
              <lod   column='[{DS_C}].[none:CountyFIPS:nk]' />
            </encodings>
          </pane>
        </panes>
        <rows>[{DS_C}].[Latitude (generated)]</rows>
        <cols>[{DS_C}].[Longitude (generated)]</cols>
      </table>
    </worksheet>
    <worksheet name='Top 20 Bar Chart'>
      <layout-options>
        <title><formatted-text><run fontname='Tableau Semibold'>Top Counties by Measure</run></formatted-text></title>
      </layout-options>
      <table>
        <view>
          <datasources>
            <datasource caption='CDC Places County' name='{DS_C}' />
            <datasource name='Parameters' />
          </datasources>
{param_dep()}
          <datasource-dependencies datasource='{DS_C}'>
            <column datatype='string' name='[LocationName]' role='dimension' type='nominal' />
            <column datatype='string' name='[StateAbbr]'    role='dimension' type='nominal' />
{calc_col()}
            <column-instance column='[LocationName]' derivation='None'
                             name='[none:LocationName:nk]' pivot='key' type='nominal' />
            <column-instance column='[StateAbbr]'    derivation='None'
                             name='[none:StateAbbr:nk]' pivot='key' type='nominal' />
            <column-instance column='{CALC}' derivation='User'
                             name='{CALC_USR}' pivot='key' type='quantitative' />
          </datasource-dependencies>
          <sort class='computed' column='[{DS_C}].[none:LocationName:nk]'
                direction='DESC' using='[{DS_C}].{CALC_USR}' />
          <aggregation value='true' />
        </view>
        <style />
        <panes>
          <pane>
            <view><breakdown value='auto' /></view>
            <mark class='Bar' />
            <encodings>
              <color column='[{DS_C}].[none:StateAbbr:nk]' />
              <text  column='[{DS_C}].{CALC_USR}' />
            </encodings>
          </pane>
        </panes>
        <rows>[{DS_C}].[none:LocationName:nk]</rows>
        <cols>[{DS_C}].{CALC_USR}</cols>
      </table>
    </worksheet>
    <worksheet name='Scatter Obesity vs Diabetes'>
      <layout-options>
        <title><formatted-text><run fontname='Tableau Semibold'>Obesity vs Diabetes (R²≈0.74)</run></formatted-text></title>
      </layout-options>
      <table>
        <view>
          <datasources>
            <datasource caption='CDC Places County' name='{DS_C}' />
          </datasources>
          <datasource-dependencies datasource='{DS_C}'>
            <column datatype='real'   name='[Diabetes_AdjPrev]' role='measure'    type='quantitative' />
            <column datatype='real'   name='[Obesity_AdjPrev]'  role='measure'    type='quantitative' />
            <column datatype='string' name='[StateDesc]'         role='dimension'
                    semantic-role='[State].[Name]' type='nominal' />
            <column datatype='string' name='[LocationName]'      role='dimension'  type='nominal' />
            <column-instance column='[Diabetes_AdjPrev]' derivation='None'
                             name='[none:Diabetes_AdjPrev:qk]' pivot='key' type='quantitative' />
            <column-instance column='[Obesity_AdjPrev]'  derivation='None'
                             name='[none:Obesity_AdjPrev:qk]'  pivot='key' type='quantitative' />
            <column-instance column='[StateDesc]'         derivation='None'
                             name='[none:StateDesc:nk]'   pivot='key' type='nominal' />
            <column-instance column='[LocationName]'      derivation='None'
                             name='[none:LocationName:nk]' pivot='key' type='nominal' />
          </datasource-dependencies>
          <aggregation value='true' />
        </view>
        <style />
        <panes>
          <pane>
            <view><breakdown value='auto' /></view>
            <mark class='Circle' />
            <encodings>
              <color column='[{DS_C}].[none:StateDesc:nk]' />
              <lod   column='[{DS_C}].[none:LocationName:nk]' />
            </encodings>
          </pane>
        </panes>
        <rows>[{DS_C}].[none:Diabetes_AdjPrev:qk]</rows>
        <cols>[{DS_C}].[none:Obesity_AdjPrev:qk]</cols>
      </table>
    </worksheet>
    <worksheet name='National Heatmap'>
      <layout-options>
        <title><formatted-text><run fontname='Tableau Semibold'>State-Level Health Heatmap</run></formatted-text></title>
      </layout-options>
      <table>
        <view>
          <datasources>
            <datasource caption='Heatmap State Conditions' name='{DS_H}' />
          </datasources>
          <datasource-dependencies datasource='{DS_H}'>
            <column datatype='string' name='[StateDesc]' role='dimension'
                    semantic-role='[State].[Name]' type='nominal' />
            <column datatype='string' name='[Condition]' role='dimension'  type='nominal' />
            <column datatype='real'   name='[Value]'     role='measure'    type='quantitative' />
            <column-instance column='[StateDesc]' derivation='None'
                             name='[none:StateDesc:nk]' pivot='key' type='nominal' />
            <column-instance column='[Condition]' derivation='None'
                             name='[none:Condition:nk]' pivot='key' type='nominal' />
            <column-instance column='[Value]'     derivation='Avg'
                             name='[avg:Value:qk]' pivot='key' type='quantitative' />
          </datasource-dependencies>
          <sort class='computed' column='[{DS_H}].[none:StateDesc:nk]'
                direction='DESC' using='[{DS_H}].[avg:Value:qk]' />
          <aggregation value='true' />
        </view>
        <style />
        <panes>
          <pane>
            <view><breakdown value='auto' /></view>
            <mark class='Square' />
            <encodings>
              <color column='[{DS_H}].[avg:Value:qk]' />
              <text  column='[{DS_H}].[avg:Value:qk]' />
            </encodings>
          </pane>
        </panes>
        <rows>[{DS_H}].[none:StateDesc:nk]</rows>
        <cols>[{DS_H}].[none:Condition:nk]</cols>
      </table>
    </worksheet>
  </worksheets>

  <!-- ════════════════════════════════════════════════════════════ -->
  <!-- DASHBOARD                                                    -->
  <!-- ════════════════════════════════════════════════════════════ -->
  <dashboards>
    <dashboard name='Public Health Dashboard'>
      <layout-options>
        <title><formatted-text>
          <run fontname='Tableau Bold' fontsize='15'>Comprehensive Public Health Analytics Dashboard</run>
        </formatted-text></title>
      </layout-options>
      <size maxheight='900' maxwidth='1400' minheight='900' minwidth='1400' />
      <zones>
        <zone h='100000' id='1' type='layout-basic' w='100000' x='0' y='0'>
          <zone h='5000'  id='2' type='title' w='100000' x='0' y='0' />
          <zone h='47500' id='3' name='County Map'        show-title='true' w='60000' x='0'     y='5000' />
          <zone h='47500' id='4' name='Top 20 Bar Chart'  show-title='true' w='40000' x='60000' y='5000' />
          <zone h='47500' id='5' name='Scatter Obesity vs Diabetes' show-title='true' w='50000' x='0'     y='52500' />
          <zone h='47500' id='6' name='National Heatmap'            show-title='true' w='50000' x='50000' y='52500' />
        </zone>
      </zones>
    </dashboard>
  </dashboards>

  <windows source-height='32'>
    <window class='dashboard' maximized='true' name='Public Health Dashboard'>
      <viewpoints>
        <viewpoint name='County Map' />
        <viewpoint name='Top 20 Bar Chart' />
        <viewpoint name='Scatter Obesity vs Diabetes' />
        <viewpoint name='National Heatmap' />
      </viewpoints>
      <active id='-1' />
    </window>
  </windows>

</workbook>
"""

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    f.write(twb)

print(f"✓ Generated: {OUT}")
print(f"  Size: {os.path.getsize(OUT)//1024} KB")
print("  → File > Open in Tableau Desktop")
