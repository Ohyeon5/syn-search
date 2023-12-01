<script>
  import { onMount } from "svelte";

  let URLAPI;
  let data;

  let requestOptions = {
    model_name: "gpt-35-turbo",
    input_text: "",
  };

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
    // URLAPI ="0.0.0.0:8000/api/chat";
    // URLAPI =
    //   window.location.protocol + "//" + window.location.hostname + ":8000/api/chat";
    console.log(URLAPI);
  });
</script>

<main>
  <div>
    <form
      on:submit|preventDefault={handleFetch}
    >
      <input
        type="text"
        placeholder="Input your reaction in smiles format"
        bind:value={requestOptions.input_text}
      />
      <button on:click|preventDefault={handleFetch}>GO</button>
    </form>
    {#if !data}
      waiting ...
    {:else}
      {data}
    {/if}
  </div>
</main>
