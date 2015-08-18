#!/usr/local/bin/fish

while true
  curl -H "Accept: application/json" -H "Content-Type: application/json" http://tds.shovik.com/toilets
  echo
  sleep 1
end

