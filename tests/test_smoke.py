from agent.agent import answer

def test_smoke_ada_lovelace():
    out = answer("Who is Ada Lovelace?")
    assert isinstance(out, str)

def test_smoke_alan_turing():
    out = answer("Who is Alan Turing?")
    assert isinstance(out, str)

def test_smoke_calc_addition():
    out = answer("What is 1 + 1?")
    assert out == 2

def test_smoke_calc_average():
    out = answer("What is the average of 4 and 6?")
    assert out == 5

def test_smoke_calc_percent():
    out = answer("What is 10 percent of 50?")
    assert out == 5

def test_smoke_weather_temperature_dhaka():
    out = answer("What's the temperature in Dhaka?")
    assert out == 31

def test_smoke_weather_condition_london():
    out = answer("What's the weather in London?")
    assert isinstance(out, str)

def test_smoke_weather_unknown_city():
    out = answer("What's the temperature in Unknown City?")
    assert out == 18

def test_smoke_job_search_software_engineer():
    out = answer("Find software engineer jobs in Dhaka")
    assert isinstance(out, list)

def test_smoke_multiple_steps():
    out = answer("Calculate 2 * 3 and check London weather")
    assert isinstance(out, float)

def test_smoke_no_plan():
    out = answer("Unknown query")
    assert out == "Sorry, I could not find an answer."

def test_smoke_invalid_tool():
    out = answer("Run invalid tool")
    assert out == "Sorry, I could not find an answer."