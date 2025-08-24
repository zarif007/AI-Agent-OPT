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

def test_calc_division_by_zero():
    out = answer("What is 10 divided by 0?")
    assert out == float('inf')

def test_calc_large_numbers():
    out = answer("What is 1000000 times 1000000?")
    assert out == 1000000000000

def test_calc_negative_numbers():
    out = answer("What is -5 plus -10?")
    assert out == -15

def test_calc_multiple_operations():
    out = answer("What is 2 plus 3 times 4?")
    assert out == 14

def test_calc_parentheses():
    out = answer("What is (2 plus 3) times 4?")
    assert out == 20

def test_weather_unknown_city_default():
    out = answer("What's the weather in Atlantis?")
    assert out == "mild cloudy"

def test_temp_city_case_insensitive():
    out = answer("What's the temperature in DhAkA?")
    assert out == 31

def test_weather_unknown_keyword():
    out = answer("What's the humidity in Paris?")
    assert out == 18  

def test_kb_not_found():
    out = answer("Who is John Doe?")
    assert out == "Sorry, I could not find an answer."

def test_kb_case_insensitive():
    out = answer("Who is ada lovelace?")
    assert isinstance(out, str)

def test_job_search_role_only():
    out = answer("Find developer jobs")
    assert isinstance(out, list)

def test_job_search_location_only():
    out = answer("Find jobs in Germany")
    assert isinstance(out, list)

def test_job_search_company_only():
    out = answer("Find jobs at Google")
    assert isinstance(out, list)

def test_job_search_date_only():
    out = answer("Find jobs posted 24h")
    assert isinstance(out, list)

def test_job_search_all_params():
    out = answer("Find software engineer jobs in Dhaka at Optimizly posted 24h")
    assert isinstance(out, list)

def test_multiple_tools_calc_and_weather():
    out = answer("What is 2 plus 2 and what's the weather in Paris?")
    assert isinstance(out, float)

def test_multiple_tools_calc_and_kb():
    out = answer("What is 2 plus 2 and who is Ada Lovelace?")
    assert isinstance(out, float)

def test_empty_string():
    out = answer("")
    assert out == "Sorry, I could not find an answer."

def test_none_input():
    out = answer(None)
    assert out == "Sorry, I could not find an answer."

def test_gibberish_input():
    out = answer("asdkjhasd 12312 !@#")
    assert out == "Sorry, I could not find an answer."

def test_multi_tool_add_to_average_temperature_case_insensitive():
    out = answer("add 10 to the average temperature in paris and london right now")
    assert abs(out - 27.5) < 1e-6

def test_multi_tool_average_temp_and_weather():
    out = answer("The average temperature in Paris and London add the temperature in Dhaka?")
    assert out == 48.5

def test_multi_tool_calc_and_job_search():
    out = answer("What is 5 times 5 and find software engineer jobs in Dhaka?")
    assert isinstance(out, list)

def test_calc_malformed_expression():
    out = answer("What is 2 + * 3?")
    assert out == 6

def test_calc_huge_expression():
    expr = " + ".join(["1"] * 10000)  
    out = answer(f"What is {expr}?")
    assert out == 10000

def test_weather_missing_args():
    out = answer("What's the weather?")
    assert isinstance(out, str)

def test_job_search_missing_args():
    out = answer("Find jobs")
    assert isinstance(out, list)

def test_kb_empty_context():
    out = answer("Who is ?")
    assert isinstance(out, str)