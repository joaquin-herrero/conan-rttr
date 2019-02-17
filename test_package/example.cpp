#include <iostream>
#include "rttr/registration"

using namespace rttr;

enum class color
{
  red,
  green,
  blue
};

RTTR_REGISTRATION
{
  rttr::registration::enumeration<color>("color")
  (
    value("red", color::red),
    value("blue", color::blue),
    value("green", color::green)
  );
}

int main() {
  type t = type::get<color>();
  
  if( !t.is_valid() )
    return 1;

  if( t.get_name() != "color" )
    return 1;

  if( !t.is_enumeration() )
    return 1;

  auto e = t.get_enumeration();

  if( e.get_values().size() != 3 )
    return 1;

  return 0;
}
