from openai import OpenAI

def compare_semantics(LLM_Output, Ground_truth_Passage):
  """ Takes in two passages of text and outputs analysis of semantic relationships
  """

  client = OpenAI()

  # LLM_Ouput -> list of claims
  claim_completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": "You take in a passage and output the claims that are made by the passage. Number them 1. 2. and so forth. Make sure claims are as granular as possible. Make sure to cover all claims, even if hidden within another claim. Be as specific as possible (with exact values, names, numbers, etc.) and provide full context (list values, names, etc.) within each claim. If no concrete claims are made, respond with NA. Follow these input output examples.\nThere are over 1,400 species of bats, making them the second most diverse order of mammals after rodents.\n1. There are over 1,400 species of bats.\n2. Bats are the second most diverse order of mammals.\n3. The most diverse order of mammals is rodents.\n\nJoe ate a quarter of the pizza. Jill ate the rest.\n1. Joe ate a quarter of the pizza.\n2. Jill ate three quarters of the pizza."},
      {"role": "user", "content": LLM_Output}
    ]
  )

  claims = claim_completion.choices[0].message.content

  # list of claims -> list of claims with eval (i.e. compared against ground truth)
  if claims == "NA":
      return "Neutral"
  else:
      claim_list = claims.split('\n')
      output = ""
      # for each claim, obtain semantic relationship with respect to the ground truth
      for claim in claim_list:

        comparison = f"Claim: {claim[3:]}\nGround Truth: {Ground_truth_Passage}"

        compare_completion = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You take in a claim and ground truth text and you determine if the claim is consistent, contradicting, or neutral with respect to the groundtruth. Pay attention to the subject and object of each claim and respond with Neutral when the ground truth does not contain directly relevant information to the claim. Only respond with Consistent, Contradicting, or Neutral."},
                {"role": "user", "content": comparison}
            ]
        )

        eval = compare_completion.choices[0].message.content

        output += f"{claim} {eval}\n"
      
      return output[:-1]
  