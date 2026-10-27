-- Read declarative gameplay records; icon helpers are intentionally discarded.
-- Run: lua tools/extract_prototypes.lua /path/to/wube/factorio-data > /tmp/prototypes.json
local root = assert(arg[1], 'Pass the factorio-data checkout directory')
data = {raw = {}}
function data:extend(records)
  for _,record in ipairs(records) do
    self.raw[record.type] = self.raw[record.type] or {}
    assert(not self.raw[record.type][record.name], 'Duplicate prototype '..record.name)
    self.raw[record.type][record.name] = record
  end
end
util = setmetatable({}, {__index=function(_,key)
  assert(key:match('^technology_icon_constant_'), 'Unexpected util helper '..key)
  return function() return {} end
end})
for _,name in ipairs({'recipe','technology','fluid','custom-inputs'}) do
  dofile(root..'/base/prototypes/'..name..'.lua')
end
local function quote(s)
  return '"'..s:gsub('[%z\1-\31\\"]',function(c)
    return string.format('\\u%04x',string.byte(c))
  end)..'"'
end
local function encode(v)
  if type(v)=='string' then return quote(v) end
  if type(v)=='number' or type(v)=='boolean' then return tostring(v) end
  if type(v)=='nil' then return 'null' end
  assert(type(v)=='table', 'Unexpected value type '..type(v))
  local array = #v>0
  local out={}
  if array then
    for _,x in ipairs(v) do out[#out+1]=encode(x) end
    return '['..table.concat(out,',')..']'
  end
  local keys={};for k in pairs(v) do keys[#keys+1]=k end;table.sort(keys)
  for _,k in ipairs(keys) do out[#out+1]=quote(k)..':'..encode(v[k]) end
  return '{'..table.concat(out,',')..'}'
end
print(encode(data.raw))
