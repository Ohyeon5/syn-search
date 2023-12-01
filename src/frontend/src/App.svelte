<script>
  import { onMount } from "svelte";

  let URLAPI;
  let data;

  let requestOptions = {
    model_name: "gpt-35-turbo",
    input_text: "",
  };

  let smiles = '';
  let additionalText = '';

  const handleFetch = async () => {
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
      URLAPI =window.location.protocol + "//"+"0.0.0.0:8000/api/chat";
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
        <input type="text" placeholder="Reaction SMILES" bind:value={smiles} />
        <button on:click|preventDefault={drawSmiles}>Draw</button>
      </div>
      <div class="additional-text">
        <input type="text" placeholder="Additional text (optional)" bind:value={additionalText} />
      </div>
      <input
        type="text"
        placeholder="Ask SynSearch"
        bind:value={requestOptions.input_text}
      />
      <button on:click|preventDefault={handleFetch}>GO</button>
    </form>
    {#if !data}
      Waiting for a response ...
    {:else}
      {data}
    {/if}
  </div>
</main>

