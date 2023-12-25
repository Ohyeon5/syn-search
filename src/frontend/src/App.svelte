<script>
  import { onMount } from "svelte";

  let URLAPI;
  let data = null;

  let requestOptions = {
    model_name: "gpt-4",
    input_text: "",
  };

  let smiles = '';
  let additionalText = '';

  const handleFetch = async () => {
    requestOptions.input_text = `You are an AI Chemistry assistant. ${smiles} ${additionalText}. Give actionable insight into this and separate each bullet point with a new line.`;
    console.log("here", URLAPI);
    data = false
    const response = await fetch(URLAPI, {
      method: "POST",
      headers: {
        accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify(requestOptions),
    });
    data = await response.json();
    data = data.choices[0].message.content
    return;
  };

  $: console.log(data);
  $: requestOptions.input_text;

  onMount(() => {
    if (window.location.hostname.includes("localhost")){
      URLAPI =
      window.location.protocol + "//" + window.location.hostname + ":8000/api/chat";
    } else {
      URLAPI =window.location.protocol + "//" + window.location.hostname + "/api/chat";
    }
    console.log(URLAPI);
  });
</script>

<main>
  <div class="top-panel">
    <button class="about-btn">About Syn Search</button>
    <div class="icon"></div>
  </div>
  <div class="input-window">
    <form on:submit|preventDefault={handleFetch}>
      <div class="smiles-input">
        <label for="reaction-smiles">Ask SynSearch</label>
        <input id="reaction-smiles" type="text" placeholder="Reaction SMILES" bind:value={smiles} />
        <button>Draw</button>
      </div>
      <div class="additional-text">
        <input type="text" placeholder="Additional text (optional)" bind:value={additionalText} />
      </div>
      <button on:click|preventDefault={handleFetch}>GO</button>
    </form>

    <div class="data-output">
      {#if !data}
        Waiting for a response ...
      {:else}
        {data}
      {/if}
    </div>
  </div>
</main>
