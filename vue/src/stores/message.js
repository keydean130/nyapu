import { defineStore } from "pinia";

export const useMessageStore = defineStore({
  id: "message",
  state: () => ({
    // メッセージレベル
    level: null,
    // メッセージ（複数メッセージを管理）
    messages: [],
  }),
  getters: {
    isError: (state) => state.level === "error",
    isWarning: (state) => state.level === "warning",
    isInfo: (state) => state.level  === "info",
  },
  actions: {
    /**
    * Errorオブジェクトを使ってエラーメッセージをセット
    */
    setError(errorObj) {
      this.level = errorObj.level || "error";
      this.message = errorObj.message || [errorObj.message];
    },
    /**
    * エラーメッセージをセット
    */
    setErrorMessage(errorObj) {
      this.level = "error";
      this.messages = [message];
    },
    /**
    * ワーニングメッセージ(複数)をセット
    */
    setWarningMessage(message) {
      this.level = "warning";
      this.messages = messages;
    },
    /**
    * インフォメーションメッセージをセット
    */
    setInfoMessage(message) {
      this.level = "info";
      this.messages = [message];
    },
    /**
    * 全メッセージをクリア
    */
    clear() {
      this.level = null;
      this.messages = [];
    },
  },
});
